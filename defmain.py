import vlans_rd
import get_interface
path01 = "script.txt"

list_vlans = vlans_rd.get_vlans()
print(list_vlans)
pevlan = list_vlans[0]
cevlan_list = list_vlans[1]
route_distinguisher = vlans_rd.get_route_distinguisher(pevlan)

service_name = str(input("Digite o nome do Serviço (Designação ou Host): "))

service_name = f"VL{pevlan}-VSI-{service_name}"

interface = get_interface.get_interface()

def first_switch():

    base_string = f"""vsi {service_name}
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

    with open(path01, 'a') as arquivo:
            arquivo.write("---------- PRIMEIRO SWITCH ----------\n")
            print(first_switch)
            arquivo.write(first_switch)


first_switch()