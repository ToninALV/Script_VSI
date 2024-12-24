import time

hostname = ["BDP-CEN-01-BNG-005","BET-GUA-01-BNG-003","CEM-TLP-01-BNG-009","DVL-VSA-01-BNG-014","CPO-ANT-01-BNG-004","IRP-CAN-01-BNG-005","LPT-CEN-01-BNG-004","PDS-JARF-01-BNG-007","SDT-CEN-01-BNG-005"]
ips = ["177.73.193.38","177.73.193.32","177.73.193.48","177.73.193.11","177.73.193.35","177.73.193.0","177.73.193.3","177.73.193.6","177.73.193.26"]


service_name = str(input("Digite o nome do Serviço (Designação ou Host): "))
vlan = int(input("Digite a VLAN: "))

service_name = f"VL{vlan}-VSI-{service_name}"


primary_host = input("Qual o Host Primário? ")
def interface ():
    interface = input("Qual a interface? ")
    speed_interface = int(input("Qual a modulação da Interface? "))
    if speed_interface == 1:
        interface = f"GigabitEthernet 0/0/{interface}"
    elif speed_interface == 10:
        interface = f"XGigabitEthernet 0/0/{interface}"
    elif speed_interface == 100:
        interface = f"100GE 0/0/{interface}"
    else:
        pass

    return interface


cevlan = int(input("Digite a vlan em que os clientes estão autenticados: "))
primary_f1a = input("Selecione o F1A Primário: ")


def menu ():
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
    match host:
        case 1:
            host = ips[0]
            print(f"Você selecionou {hostname[0]}!")
        case 2:
            host = ips[1]
            print(f"Você selecionou {hostname[1]}!")
        case 3:
            host = ips[2]
            print(f"Você selecionou {hostname[2]}!")
        case 4:
            host = ips[3]
            print(f"Você selecionou {hostname[3]}!")
        case 5:
            host = ips[4]
            print(f"Você selecionou {hostname[4]}!")
        case 6:
            host = ips[5]
            print(f"Você selecionou {hostname[5]}!")
        case 7:
            host = ips[6]
            print(f"Você selecionou {hostname[6]}!")
        case 8:
            host = ips[7]
            print(f"Você selecionou {hostname[7]}!")
        case 9:
            host = ips[8]
            print(f"Você selecionou {hostname[8]}!")
        case _:
            print("Opção Inválida, Tente Novamente!!!")
            return menu()

    return host

e_trunk = input("Possuí e-trunk? (S/N) ").upper()


print("----- Criando Script -----")
time.sleep(1)


print(f""" 

### Comando para o Primeiro Switch ###      
      
vsi {service_name}
    pwsignal bgp
    route_distinguisher 28198:{vlan}
    vpn-target 28198:{vlan} import-extcommunity
    vpn-target 28198:{vlan} export-extcommunity
    site 1 range 5 default-offset 1
    quit


interface {interface}.{vlan}
    description {service_name}
    qinq stacking vid {cevlan} pe-vid {vlan}
    qinq stacking vid {cevlan} pe-vid {vlan}
    qinq stacking vid {cevlan} pe-vid {vlan}
    l2 binding vsi {service_name}


### Comandor para o Switch com F1A ###




""")








