import time
import os
import paramiko


hostname = ["BDP-CEN-01-BNG-005","BET-GUA-01-BNG-003","CEM-TLP-01-BNG-009","DVL-VSA-01-BNG-014","CPO-ANT-01-BNG-004","IRP-CAN-01-BNG-005","LPT-CEN-01-BNG-004","PDS-JARF-01-BNG-007","SDT-CEN-01-BNG-005"]


path01 = "script.txt"


try:
    os.remove(path01)

except:
    pass


def get_vlans():
    cevlan_list = []

    pevlan = input("Digite a PEVLAN: ")
    if pevlan.isdigit():
        pass
    else:
        print("Valor digitado não é válido, Tente Novamente!")
        pass

    cevlan = input("Digite a CEVLAN: ")
    if cevlan.isdigit():
        cevlan_list.append(cevlan)
        pass
    else:
        print("Valor digitado não é válido, Tente Novamente!")
        pass
    while True:
        option = input("Deseja inserir mais CEVLAN ? (S/N): ").upper()
        if option == "S":
            cevlan = input("Digite a CEVLAN: ")
            if cevlan.isdigit():
                cevlan_list.append(cevlan)
                pass
            else:
                print("Opção Inválida, Tente Novamente!")
        elif option == "N":
            break
        else:
            print("Opção Inválida, Tente Novamente!")
            pass
    list_vlans = [pevlan, cevlan_list]

    return list_vlans


e_trunk = input("Possuí e-trunk? (S/N) ").upper()

def connect_equipament(command):
    host = "10.128.44.3"
    port = "6422"
    username = "antonio.silva"
    password = "An@13606973659"
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port=port, username=username, password=password)
        print("----- PESQUISANDO ROUTE DISTINGUISHER -----")
    except:
        print("**CONEXÃO NÃO ESTABELECIDA**")


    stdin, stdout, stderr = ssh.exec_command(command)
    stdout = stdout.read().decode('ascii').strip("\n")
    terminal = stdout
    terminal = str(stdout)

    ssh.close()


    return terminal


def get_route_distinguisher(vlan):
    for i in range(1,100):
        
        command = f"""display bgp l2vpn-ad routing-table vpls route-distinguisher {i}{vlan}\n"""
        result = connect_equipament(command)
        if "NextHop" in result:
            pass
        else:
            route_distinguisher = f"28198:{i}{vlan}"
            break

    return route_distinguisher


def menu (host):
    match host:
        case 1: #BOM DESPACHO#
            interface_pppoe = "Eth-Trunk6"
            interface_type = "trunk"
            conc_secondary = "PDS-JARF-01-BNG-007"
            interface_pppoe_secondary = "Eth-Trunk2"
            interface_type_secondary = "trunk"
            conc_tertiary = "LPT-CEN-01-BNG-004"
            interface_pppoe_tertiary= ""
            interface_type_tertiary = ""
            print(f"Você selecionou {hostname[0]}!")
            
        case 2: #BETIM#
            interface_pppoe = "Eth-Trunk6"
            interface_type = "trunk"
            conc_secondary = "CEM-TLP-01-BNG-009"
            interface_pppoe_secondary = "Eth-Trunk15"
            interface_type_secondary = "hybrid"
            conc_tertiary = "PDS-JARF-01-BNG-007"
            interface_pppoe_tertiary= "Eth-Trunk2"
            interface_type_tertiary = "trunk"
            print(f"Você selecionou {hostname[1]}!")
        case 3: #TELEPORTO#
            interface_pppoe = "Eth-Trunk15"
            interface_type = "hybrid"
            conc_secondary = "DVL-VSA-01-BNG-014"
            interface_pppoe_secondary = "Eth-Trunk2"
            interface_type_secondary = "hybrid"
            conc_tertiary = "PDS-JARF-01-BNG-007"
            interface_pppoe_tertiary= "Eth-Trunk2"
            interface_type_tertiary = "trunk"
            print(f"Você selecionou {hostname[2]}!")
        case 4: #DIVINÓPOLIS#
            interface_pppoe = "Eth-Trunk2"
            interface_type = "hybrid"
            conc_secondary = "LPT-CEN-01-BNG-004"
            interface_pppoe_secondary = ""
            interface_type_secondary = ""
            conc_tertiary = "CEM-TLP-01-BNG-009"
            interface_pppoe_tertiary= "Eth-Trunk15"
            interface_type_tertiary = "hybrid"
            print(f"Você selecionou {hostname[3]}!")
        case 5: #CAMPO BELO#
            interface_pppoe = "Eth-Trunk8"
            interface_type = "hybrid"
            conc_secondary = "CEM-TLP-01-BNG-009"
            interface_pppoe_secondary = "Eth-Trunk15"
            interface_type_secondary = "hybrid"
            conc_tertiary = "PDS-JARF-01-BNG-007"
            interface_pppoe_tertiary= "Eth-Trunk2"
            interface_type_tertiary = "trunk"
            print(f"Você selecionou {hostname[4]}!")
        case 6: #IGARAPÉ#
            interface_pppoe = "Eth-Trunk1"
            interface_type = "trunk"
            conc_secondary = "CEM-TLP-01-BNG-009"
            interface_pppoe_secondary = "Eth-Trunk15"
            interface_type_secondary = "hybrid"
            conc_tertiary = "PDS-JARF-01-BNG-007"
            interface_pppoe_tertiary= "Eth-Trunk2"
            interface_type_tertiary = "trunk"
            print(f"Você selecionou {hostname[5]}!")
        case 7: #LAGOA DA PRATA#
            interface_pppoe = "Eth-Trunk2"
            interface_type = "trunk"
            conc_secondary = "PDS-JARF-01-BNG-009"
            interface_pppoe_secondary = "Eth-Trunk2"
            interface_type_secondary = "trunk"
            conc_tertiary = "DVL-VSA-01-BNG-014"
            interface_pppoe_tertiary = "Eth-Trunk2"
            interface_type_tertiary = "hybrid"
            print(f"Você selecionou {hostname[6]}!")
        case 8: #PERDÕES#
            interface_pppoe = "Eth-Trunk2"
            interface_type = "trunk"
            conc_secondary = "LPT-CEN-01-BNG-004"
            interface_pppoe_secondary = ""
            interface_type_secondary = ""
            conc_tertiary = "DVL-VSA-01-BNG-014"
            interface_pppoe_tertiary = "Eth-Trunk2"
            interface_type_tertiary = "hybrid"
            print(f"Você selecionou {hostname[7]}!")
        case 9: #SAMONTE#
            interface_pppoe = "Eth-Trunk6"
            interface_type = "trunk"
            conc_secondary = "CEM-TLP-01-BNG-009"
            interface_pppoe_secondary = "Eth-Trunk15"
            interface_type_secondary = "hybrid"
            conc_tertiary = "LPT-CEN-01-BNG-004"
            interface_pppoe_tertiary = ""
            interface_type_tertiary = ""
            print(f"Você selecionou {hostname[8]}!")
        case _:
            print("Opção Inválida, Tente Novamente!!!")
            return menu()
        
    return interface_pppoe, interface_type, conc_secondary, interface_pppoe_secondary, interface_type_secondary, conc_tertiary, interface_pppoe_tertiary, interface_type_tertiary

def main():

    
    list_vlans = get_vlans()
    print(list_vlans)
    pevlan = list_vlans[0]
    cevlan_list = list_vlans[1]
    route_distinguisher = get_route_distinguisher(pevlan)


    service_name = str(input("Digite o nome do Serviço (Designação ou Host): "))

    service_name = f"VL{pevlan}-VSI-{service_name}"

    interface = input("Qual a interface? ")
    speed_interface = int(input("Qual a modulação da Interface? (1G/10G/100G/eth) "))
    if speed_interface == 1:
        interface = f"GigabitEthernet 0/0/{interface}"
    elif speed_interface == 10:
        interface = f"XGigabitEthernet 0/0/{interface}"
    elif speed_interface == 100:
        interface = f"100GE 0/0/{interface}"
    elif speed_interface == "eth":
         interface = f"Eth-trunk{interface}"
    else:
        pass

    print("""
----- LOCAIS DE AUTENTICAÇÃO -----
          
(1) BOM DESPACHO
(2) BETIM
(3) TELEPORTO
(4) DIVINÓPOLIS
(5) CAMPO BELO
(6) IGARAPÉ
(7) LAGOA DA PRATA
(8) PERDÕES
(9) SAMONTE
""")
    host = int(input("Selecione o local de autenticação: "))  
    interface_pppoe, interface_type, conc_secondary, interface_pppoe_secondary, interface_type_secondary, conc_tertiary, interface_pppoe_tertiary, interface_type_tertiary = menu(host) 

    #Construção comandos primeiro Switch
    base_string = f"""vsi {service_name}
 pwsignal bgp
  route-distinguisher {route_distinguisher}
  vpn-target {route_distinguisher} import-extcommunity
  vpn-target {route_distinguisher} export-extcommunity
  site 1 range 5 default-offset 1


interface {interface}.{pevlan}
    description {service_name}"""

    qinq_lines = "\n".join([f" qinq stacking vid {cevlan} pe-vid {pevlan}" for cevlan in cevlan_list])

    first_switch = f"{base_string}\n{qinq_lines}\n l2 binding vsi {service_name}\n\n"

    with open(path01, 'a') as arquivo:
            arquivo.write("---------- PRIMEIRO SWITCH ----------\n")
            arquivo.write(first_switch)

    #Construção comandos primeiro switch com F1A

    base_string = f"""vsi {service_name}
 pwsignal bgp
  route-distinguisher {route_distinguisher}
  vpn-target {route_distinguisher} import-extcommunity
  vpn-target {route_distinguisher} export-extcommunity
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

    with open(path01, 'a') as arquivo:
            arquivo.write("---------- SEGUNDO SWITCH ----------\n")
            arquivo.write(second_switch)

    #Construção Comandos para o primeiro F1A

    base_string = f"""interface Eth-Trunk0.{pevlan}
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
    
    with open(path01, 'a') as arquivo:
            arquivo.write("---------- PRIMEIRO F1A ----------\n")
            arquivo.write(first_f1a)

    #Construção comandos para o segundo switch com F1A

    base_string = f"""vsi {service_name}
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
    second_switch = f"{base_string}\n{port_line}\n\n"

    with open(path01, 'a') as arquivo:
            arquivo.write("---------- SEGUNDO SWITCH COM F1A ----------\n")
            arquivo.write(second_switch)

    #Construção comandos para o segundo F1A7

    base_string = f"""interface Eth-Trunk0.{pevlan}
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
    
    with open(path01, 'a') as arquivo:
            arquivo.write(f"---------- SEGUNDO F1A {conc_secondary} ----------\n")
            arquivo.write(second_f1a)

    #Construção comandos para o terceiro switch com F1A

    base_string = f"""vsi {service_name}
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

interface {interface_pppoe_tertiary}"""
    if interface_type_tertiary == "trunk":
        port_line = "port trunk allow-pass vlan "
    elif interface_type_tertiary == "hybrid":
        port_line = "port hybrid tagged vlan "
    else:
        pass

    port_line = f"{port_line}{pevlan}"
    thirdy_switch = f"{base_string}\n{port_line}\n\n"

    with open(path01, 'a') as arquivo:
            arquivo.write("---------- TERCEIRO SWITCH COM F1A ----------\n")
            arquivo.write(thirdy_switch)

    #Construção comandos para o terceiro F1A

    base_string = f"""interface Eth-Trunk0.{pevlan}
 description {service_name}
 ipv6 enable
 ipv6 address auto link-local
 statistic enable
 commit"""
    
    qinq_lines = "\n".join([f" user-vlan {cevlan} qinq {pevlan}" for cevlan in cevlan_list])
    thirdy_f1a = f"""{base_string}\n{qinq_lines}\nquit
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
    
    with open(path01, 'a') as arquivo:
            arquivo.write(f"---------- TERCEIRO F1A {conc_tertiary} ----------\n")
            arquivo.write(thirdy_f1a)

main()
print("----- SCRIPT FINALIZADO -----")