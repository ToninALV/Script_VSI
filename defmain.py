import vlans_rd
import get_interface
import menu


list_vlans = vlans_rd.get_vlans()
print(list_vlans)
pevlan = list_vlans[0]
cevlan_list = list_vlans[1]
route_distinguisher = vlans_rd.get_route_distinguisher(pevlan)

service_name = str(input("Digite o nome do Serviço (Designação ou Host): "))

service_name = f"VL{pevlan}-VSI-{service_name}"

interface = get_interface.get_interface()

interface_pppoe, interface_type, conc_secondary, interface_pppoe_secondary, interface_type_secondary, conc_tertiary, interface_pppoe_tertiary, interface_type_tertiary = menu.menu()

def first_switch():

    base_string = f"""
---------- PRIMEIRO SWITCH ----------\n
vsi {service_name}
 pwsignal bgp
  route-distinguisher {route_distinguisher}
  vpn-target {route_distinguisher} import-extcommunity
  vpn-target {route_distinguisher} export-extcommunity
  site 1 range 5 default-offset 1


interface {interface}.{pevlan}
    description {service_name}"""

    qinq_lines = "\n".join([f" qinq stacking vid {cevlan} pe-vid {pevlan}" for cevlan in cevlan_list])
    mtu_disable_line = "mtu-negotiate disable"
    first_switch = f"{base_string}\n{qinq_lines}\n l2 binding vsi {service_name}\n\n"


    return first_switch

def etrunk_switch():


    return None
    

def second_switch():

    if conc_secondary == "LPT-CEN-01-BNG-004":
        base_string = f"""
        ---------- SEGUNDO SWITCH ----------\n
set routing-instances {service_name} instance-type virtual-switch
set routing-instances {service_name} protocols vpls site 2 site-identifier 2
set routing-instances {service_name} protocols vpls site-range 5
set routing-instances {service_name} protocols vpls no-tunnel-services
set routing-instances {service_name} route-distinguisher {route_distinguisher}
set routing-instances {service_name} vrf-target target:{route_distinguisher}
set routing-instances {service_name} vlans {service_name} vlan-id {pevlan}
set routing-instances {service_name} vlans {service_name} interface ae6.{pevlan}

set interfaces ae6 unit {pevlan} description {service_name}
set interfaces ae6 unit {pevlan} encapsulation vlan-vpls
set interfaces ae6 unit {pevlan} vlan-id {pevlan}

set vlans {service_name} description {service_name}
set vlans {service_name} vlan-id {pevlan}

"""
        second_switch = base_string

    elif conc_secondary != "LPT-CEN-01-BNG-004" and conc_tertiary == "LPT-CEN-01-BNG-004":
        base_string = f"""
        ---------- SEGUNDO SWITCH ----------\n
vsi {service_name}
 pwsignal bgp
  route-distinguisher {route_distinguisher}
  vpn-target {route_distinguisher} import-extcommunity
  vpn-target {route_distinguisher} export-extcommunity
  mtu-negotiate disable
  site 2 range 5 default-offset 1

vlan {pevlan}
description {service_name}
quit

interface vlanif {pevlan}
description {service_name}
l2 binding vsi {service_name}

interface {interface_pppoe}"""
        if interface_type == "trunk":
            port_line = "port trunk allow-pass vlan "
        elif interface_type == "hybrid":
            port_line = "port hybrid tagged vlan "
        else:
            pass

        port_line = f"{port_line}{pevlan}"
        second_switch = f"{base_string}\n{port_line}\n\n"

    elif conc_secondary != "LPT-CEN-01-BNG-004" and conc_tertiary != "LPT-CEN-01-BNG-004":
        base_string = f"""
        ---------- SEGUNDO SWITCH ----------\n
vsi {service_name}
 pwsignal bgp
  route-distinguisher {route_distinguisher}
  vpn-target {route_distinguisher} import-extcommunity
  vpn-target {route_distinguisher} export-extcommunity2025
  site 2 range 5 default-offset 1

vlan {pevlan}
description {service_name}
quit

interface vlanif {pevlan}
description {service_name}
l2 binding vsi {service_name}

interface {interface_pppoe}"""
        if interface_type == "trunk":
            port_line = "port trunk allow-pass vlan "
        elif interface_type == "hybrid":
            port_line = "port hybrid tagged vlan "
        else:
            pass

        port_line = f"{port_line}{pevlan}"
        second_switch = f"{base_string}\n{port_line}\n\n"

    else:
        print("não foi possível identificado...")

    return second_switch


def first_f1a():
    base_string = f"""
---------- PRIMEIRO F1A ----------\n
interface Eth-Trunk0.{pevlan}
 description {service_name}
 ipv6 enable
 ipv6 address auto link-local
 statistic enable
 commit"""
    
    qinq_lines = "\n".join([f" user-vlan {cevlan} qinq {pevlan}" for cevlan in cevlan_list])
    first_f1a = f"""{base_string}\n{qinq_lines}\nquit
 pppoe-server bind Virtual-Template 1
 ipv6 nd autoconfig managed-address-flag
 ipv6 nd autoconfig other-flag
 commit
 bas
 #
  access-type layer2-subscriber default-domain authentication sempreinternet
 #
#
"""
    
    return first_f1a


def third_switch():
    if conc_secondary == "LPT-CEN-01-BNG-004" or conc_tertiary == "LPT-CEN-01-BNG-004":
        base_string = f"""
        ---------- TERCEIRO SWITCH ----------
vsi {service_name}
 pwsignal bgp
  route-distinguisher {route_distinguisher}
  vpn-target {route_distinguisher} import-extcommunity
  vpn-target {route_distinguisher} export-extcommunity
  mtu-negotiate disable
  site 4 range 5 default-offset 1

vlan {pevlan}
description {service_name}
quit

interface vlanif {pevlan}
description {service_name}
l2 binding vsi {service_name}

interface {interface_pppoe_secondary}"""
        if interface_type_secondary == "trunk":
            port_line = "port trunk allow-pass vlan "
        elif interface_type_secondary == "hybrid":
            port_line = "port hybrid tagged vlan "
        else:
            pass

        port_line = f"{port_line}{pevlan}"
        third_switch = f"{base_string}\n{port_line}\n\n"

    elif conc_secondary != "LPT-CEN-01-BNG-004" or conc_tertiary != "LPT-CEN-01-BNG-004":
        base_string = f"""
        ---------- TERCEIRO SWITCH ----------
vsi {service_name}
 pwsignal bgp
  route-distinguisher {route_distinguisher}
  vpn-target {route_distinguisher} import-extcommunity
  vpn-target {route_distinguisher} export-extcommunity
  site 4 range 5 default-offset 1

vlan {pevlan}
description {service_name}
quit

interface vlanif {pevlan}
description {service_name}
l2 binding vsi {service_name}

interface {interface_pppoe_secondary}"""
        if interface_type_secondary == "trunk":
            port_line = "port trunk allow-pass vlan "
        elif interface_type_secondary == "hybrid":
            port_line = "port hybrid tagged vlan "
        else:
            pass

        port_line = f"{port_line}{pevlan}"
        third_switch = f"{base_string}\n{port_line}\n\n"

    return third_switch

def second_f1a():
    base_string = f"""
        ---------- SEGUNDO F1A {conc_secondary} ----------
interface Eth-Trunk0.{pevlan}
 description {service_name}
 ipv6 enable
 ipv6 address auto link-local
 statistic enable
 commit"""
    
    qinq_lines = "\n".join([f" user-vlan {cevlan} qinq {pevlan}" for cevlan in cevlan_list])
    second_f1a = f"""{base_string}\n{qinq_lines}\nquit
 pppoe-server bind Virtual-Template 1
 ipv6 nd autoconfig managed-address-flag
 ipv6 nd autoconfig other-flag
 commit
 bas
 #
  access-type layer2-subscriber default-domain authentication sempreinternet
  access-delay 100
 #
#
"""
    return second_f1a


print(second_switch())



