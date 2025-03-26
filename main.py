import vlans_rd
import get_interface
import menu
import os
import sys


list_vlans = vlans_rd.get_vlans()
print(list_vlans)
pevlan = list_vlans[0]
cevlan_list = list_vlans[1]
route_distinguisher = vlans_rd.get_route_distinguisher(pevlan)

service_name = str(input("Digite o nome do Serviço (Designação ou Host): "))

service_name = f"VL{pevlan}-VSI-{service_name}"

interface = get_interface.get_interface()

conc_primary, interface_pppoe, interface_type, conc_secondary, interface_pppoe_secondary, interface_type_secondary, conc_tertiary, interface_pppoe_tertiary, interface_type_tertiary = menu.menu()

def client_switch(): #Primeiro Switch, De onde vai sair os clientes

    base_string = f"""
----------------------------------- PRIMEIRO SWITCH COM CLIENTES -----------------------------------\n
vsi {service_name}
 pwsignal bgp
  route-distinguisher {route_distinguisher}
  vpn-target {route_distinguisher} import-extcommunity
  vpn-target {route_distinguisher} export-extcommunity
  site 1 range 5 default-offset 1


interface {interface}.{pevlan}
    description {service_name}"""

    qinq_lines = "\n".join([f" qinq stacking vid {cevlan} pe-vid {pevlan}" for cevlan in cevlan_list])
    if conc_secondary == "LPT-CEN-01-MPLS" or conc_tertiary == "LPT-CEN-01-MPLS":
        client_switch = f"{base_string}\n{qinq_lines}\n l2 binding vsi {service_name}\n\n" 
    mtu_disable_line = "mtu-negotiate disable"
    client_switch = f"{base_string}\n{qinq_lines}\n l2 binding vsi {service_name}\n\n"


    return client_switch
    

def second_switch(): #Segundo Switch. 2º ponto da VSI, linkado ao primeiro BNG

    if conc_primary == "LPT-CEN-01-BNG-004":
        base_string = f"""
        ----------------------------------- SEGUNDO SWITCH -----------------------------------\n
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

    elif conc_primary != "LPT-CEN-01-BNG-004" and conc_secondary == "LPT-CEN-01-BNG-004" or conc_tertiary == "LPT-CEN-01-BNG-004":
        base_string = f"""
        ----------------------------------- SEGUNDO SWITCH -----------------------------------\n
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

    elif conc_primary != "LPT-CEN-01-BNG-004" and conc_secondary != "LPT-CEN-01-BNG-004" or conc_tertiary != "LPT-CEN-01-BNG-004":
        base_string = f"""
        ----------------------------------- SEGUNDO SWITCH -----------------------------------\n
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


def first_bng(): #Primeiro BNG, onde será feito a autenticação dos clientes.
    base_string = f"""
----------------------------------- PRIMEIRO F1A {conc_primary} -----------------------------------\n
interface Eth-Trunk0.{pevlan}
 description {service_name}
 ipv6 enable
 ipv6 address auto link-local
 statistic enable
 commit"""
    
    qinq_lines = "\n".join([f" user-vlan {cevlan} qinq {pevlan}" for cevlan in cevlan_list])
    first_bng = f"""{base_string}\n{qinq_lines}\nquit
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
    
    return first_bng


def third_switch(): #Terceiro Switch, 4º ponto da VSI, Linkado ao Segundo BNG.
    if conc_secondary == "LPT-CEN-01-BNG-004":
        base_string = f"""
        ----------------------------------- TERCEIRO SWITCH -----------------------------------\n
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
        third_switch = base_string

    elif conc_secondary != "LPT-CEN-01-BNG-004" and conc_primary == "LPT-CEN-01-BNG-004" or conc_tertiary == "LPT-CEN-01-BNG-004":
        base_string = f"""
        ----------------------------------- TERCEIRO SWITCH -----------------------------------\n
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
        third_switch = f"{base_string}\n{port_line}\n\n"

    elif conc_secondary != "LPT-CEN-01-BNG-004" and conc_primary != "LPT-CEN-01-BNG-004" or conc_tertiary != "LPT-CEN-01-BNG-004":
        base_string = f"""
        ----------------------------------- TERCEIRO SWITCH -----------------------------------\n
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
        third_switch = f"{base_string}\n{port_line}\n\n"

    else:
        print("não foi possível identificado...")

    return third_switch

def second_bng():
    base_string = f"""
        ----------------------------------- SEGUNDO F1A {conc_secondary} -----------------------------------
interface Eth-Trunk0.{pevlan}
 description {service_name}
 ipv6 enable
 ipv6 address auto link-local
 statistic enable
 commit"""
    
    qinq_lines = "\n".join([f" user-vlan {cevlan} qinq {pevlan}" for cevlan in cevlan_list])
    second_bng = f"""{base_string}\n{qinq_lines}\nquit
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
    return second_bng


def fourth_switch():
    if conc_tertiary == "LPT-CEN-01-BNG-004":
        base_string = f"""
        ----------------------------------- QUARTO SWITCH -----------------------------------\n
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
        fourth_switch = base_string

    elif conc_tertiary != "LPT-CEN-01-BNG-004" and conc_primary == "LPT-CEN-01-BNG-004" or conc_secondary == "LPT-CEN-01-BNG-004":
        base_string = f"""
        ----------------------------------- QUARTO SWITCH -----------------------------------\n
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
        fourth_switch = f"{base_string}\n{port_line}\n\n"

    elif conc_tertiary != "LPT-CEN-01-BNG-004" and conc_primary != "LPT-CEN-01-BNG-004" or conc_secondary != "LPT-CEN-01-BNG-004":
        base_string = f"""
        ----------------------------------- QUARTO SWITCH -----------------------------------\n
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
        fourth_switch = f"{base_string}\n{port_line}\n\n"

    else:
        print("não foi possível identificado...")

    return fourth_switch


def third_bng():
    base_string = f"""
        ----------------------------------- TERCEIRO F1A {conc_tertiary} -----------------------------------\n
interface Eth-Trunk0.{pevlan}
 description {service_name}
 ipv6 enable
 ipv6 address auto link-local
 statistic enable
 commit"""
    
    qinq_lines = "\n".join([f" user-vlan {cevlan} qinq {pevlan}" for cevlan in cevlan_list])
    third_f1a = f"""{base_string}\n{qinq_lines}\nquit
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
    return third_f1a


def make_script():

    ###path01 = f"Scripts/{service_name}.txt"
    caminho_pasta = get_save_path()
    caminho_arquivo = os.path.join(caminho_pasta, f"{service_name}.txt")

    switch_cliente = client_switch()
    primeiro_switch = second_switch()
    primeiro_bng = first_bng()
    segundo_switch = third_switch()
    segundo_bng = second_bng()
    terceiro_switch = fourth_switch()
    terceiro_bng = third_bng()

    with open(caminho_arquivo, 'w') as arquivo:
            arquivo.write(switch_cliente)
            arquivo.write(primeiro_switch)
            arquivo.write(primeiro_bng)
            arquivo.write(segundo_switch)
            arquivo.write(segundo_bng)
            arquivo.write(terceiro_switch)
            arquivo.write(terceiro_bng)


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_save_path():
    documentos = os.path.expanduser('~/Documents')
    scripts_path = os.path.join(documentos, 'Scripts_VSI', 'Scripts')
    os.makedirs(scripts_path, exist_ok=True)
    return scripts_path


make_script()