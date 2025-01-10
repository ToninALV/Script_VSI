hostname = ["BDP-CEN-01-BNG-005","BET-GUA-01-BNG-003","CEM-TLP-01-BNG-009","DVL-VSA-01-BNG-014","CPO-ANT-01-BNG-004","IRP-CAN-01-BNG-005","LPT-CEN-01-BNG-004","PDS-JARF-01-BNG-007","SDT-CEN-01-BNG-005"]
ips = ["177.73.193.38","177.73.193.32","177.73.193.48","177.73.193.11","177.73.193.35","177.73.193.0","177.73.193.3","177.73.193.6","177.73.193.26"]


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
        case 1: #BOM DESPACHO#
            interface_pppoe = "Eth-Trunk6"
            interface_type = "trunk"
            conc_secondary = "PDS-JARF-01-BNG-007"
            interface_pppoe_secondary = "Eth-Trunk2"
            conc_tertiary = "LPT-CEN-01-BNG-004"
            interface_pppoe_tertiary= ""
            print(f"Você selecionou {hostname[0]}!")
            host = ips[0]
            
        case 2: #BETIM#
            host = ips[1]
            interface_pppoe = "Eth-Trunk6"
            interface_type = "trunk"
            conc_secondary = "CEM-TLP-01-BNG-009"
            interface_pppoe_secondary = "Eth-Trunk15"
            conc_tertiary = "PDS-JARF-01-BNG-007"
            interface_pppoe_tertiary= "Eth-Trunk2"
            print(f"Você selecionou {hostname[1]}!")
        case 3: #TELEPORTO#
            host = ips[2]
            interface_pppoe = "Eth-Trunk15"
            interface_type = "hybrid"
            conc_secondary = "DVL-VSA-01-BNG-014"
            interface_pppoe_secondary = "Eth-Trunk2"
            conc_tertiary = "PDS-JARF-01-BNG-007"
            interface_pppoe_tertiary= "Eth-Trunk2"
            print(f"Você selecionou {hostname[2]}!")
        case 4: #DIVINÓPOLIS#
            host = ips[3]
            interface_pppoe = "Eth-Trunk2"
            interface_type = "hybrid"
            conc_secondary = "LPT-CEN-01-BNG-004"
            interface_pppoe_secondary = ""
            conc_tertiary = "CEM-TLP-01-BNG-009"
            interface_pppoe_tertiary= "Eth-Trunk15"
            print(f"Você selecionou {hostname[3]}!")
        case 5: #CAMPO BELO#
            host = ips[4]
            interface_pppoe = "Eth-Trunk8"
            interface_type = "hybrid"
            conc_secondary = "CEM-TLP-01-BNG-009"
            interface_pppoe_secondary = "Eth-Trunk15"
            conc_tertiary = "PDS-JARF-01-BNG-007"
            interface_pppoe_tertiary= "Eth-Trunk2"
            print(f"Você selecionou {hostname[4]}!")
        case 6: #IGARAPÉ#
            host = ips[5]
            interface_pppoe = "Eth-Trunk1"
            interface_type = "trunk"
            conc_secondary = "CEM-TLP-01-BNG-009"
            interface_pppoe_secondary = "Eth-Trunk15"
            conc_tertiary = "PDS-JARF-01-BNG-007"
            interface_pppoe_tertiary= "Eth-Trunk2"
            print(f"Você selecionou {hostname[5]}!")
        case 7: #LAGOA DA PRATA#
            host = ips[6]
            interface_pppoe = "Eth-Trunk6"
            interface_type = "trunk"
            conc_secondary = "PDS-JARF-01-BNG-009"
            interface_pppoe_secondary = "Eth-Trunk2"
            conc_tertiary = "DVL-VSA-01-BNG-014"
            interface_pppoe_tertiary= ""
            print(f"Você selecionou {hostname[6]}!")
        case 8: #PERDÕES#
            host = ips[7]
            interface_pppoe = "Eth-Trunk2"
            interface_type = "trunk"
            conc_secondary = "LPT-CEN-01-BNG-004"
            interface_pppoe_secondary = ""
            conc_tertiary = "DVL-VSA-01-BNG-014"
            interface_pppoe_tertiary= "Eth-Trunk2"
            print(f"Você selecionou {hostname[7]}!")
        case 9: #SAMONTE#
            host = ips[8]
            interface_pppoe = "Eth-Trunk6"
            interface_type = "trunk"
            conc_secondary = "CEM-TLP-01-BNG-009"
            interface_pppoe_secondary = "Eth-Trunk15"
            conc_tertiary = "LPT-CEN-01-BNG-004"
            interface_pppoe_tertiary= ""
            print(f"Você selecionou {hostname[8]}!")
        case _:
            print("Opção Inválida, Tente Novamente!!!")
            return menu()
        
    return interface_pppoe, interface_type, conc_secondary, interface_pppoe_secondary, conc_tertiary, interface_pppoe_tertiary

