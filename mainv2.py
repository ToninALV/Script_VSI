import os
import paramiko

def remove_existing_file(path):
    try:
        os.remove(path)
    except FileNotFoundError:
        pass

def prompt_for_vlans():
    cevlan_list = []

    while True:
        pevlan = input("Digite a PEVLAN: ")
        if pevlan.isdigit():
            break
        print("Valor digitado não é válido, Tente Novamente!")

    while True:
        cevlan = input("Digite a CEVLAN: ")
        if cevlan.isdigit():
            cevlan_list.append(cevlan)
            option = input("Deseja inserir mais CEVLAN ? (S/N): ").upper()
            if option == "N":
                break
        else:
            print("Valor digitado não é válido, Tente Novamente!")

    return pevlan, cevlan_list

def connect_to_equipment(host, port, username, password, command):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port=port, username=username, password=password)

        stdin, stdout, stderr = ssh.exec_command(command)
        result = stdout.read().decode('ascii').strip()
        ssh.close()
        return result
    except Exception as e:
        print(f"**CONEXÃO NÃO ESTABELECIDA**: {e}")
        return None

def find_route_distinguisher(vlan):
    for i in range(1, 100):
        command = f"display bgp l2vpn-ad routing-table vpls route-distinguisher {i}{vlan}\n"
        result = connect_to_equipment("10.128.44.3", 6422, "antonio.silva", "An@13606973659", command)
        if result and "NextHop" not in result:
            return f"28198:{i}{vlan}"
    return None

def select_location():
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

    while True:
        try:
            choice = int(input("Selecione o local de autenticação: "))
            if 1 <= choice <= 9:
                return choice
        except ValueError:
            pass
        print("Opção Inválida, Tente Novamente!")

def build_switch_command(service_name, pevlan, cevlan_list, interface):
    base_string = f"""vsi {service_name}
 pwsignal bgp
  route-distinguisher {pevlan}
  vpn-target {pevlan} import-extcommunity
  vpn-target {pevlan} export-extcommunity
  site 1 range 5 default-offset 1

interface {interface}.{pevlan}
    description {service_name}"""

    qinq_lines = "\n".join([f" qinq stacking vid {cevlan} pe-vid {pevlan}" for cevlan in cevlan_list])
    return f"{base_string}\n{qinq_lines}\n l2 binding vsi {service_name}\n"

def main():
    script_path = "script.txt"
    remove_existing_file(script_path)

    pevlan, cevlan_list = prompt_for_vlans()
    route_distinguisher = find_route_distinguisher(pevlan)
    service_name = f"VL{pevlan}-VSI-{input('Digite o nome do Serviço (Designação ou Host): ')}"
    interface = input("Qual a interface? ")

    switch_command = build_switch_command(service_name, pevlan, cevlan_list, interface)

    with open(script_path, 'a') as script_file:
        script_file.write("---------- PRIMEIRO SWITCH ----------\n")
        script_file.write(switch_command)

    print("----- SCRIPT FINALIZADO -----")

if __name__ == "__main__":
    main()