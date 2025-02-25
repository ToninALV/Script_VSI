import connect_ssh


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
    """list_vlans = [pevlan, cevlan_list]"""

    return [pevlan, cevlan_list]



def get_route_distinguisher(vlan):
    for i in range(1,100):
        
        command = f"""display bgp l2vpn-ad routing-table vpls route-distinguisher 28198:{i}{vlan}\n"""
        result = connect_ssh.connect_equipament(command)
        if "NextHop" in result:
            pass
        else:
            route_distinguisher = f"28198:{i}{vlan}"
            break

    return route_distinguisher