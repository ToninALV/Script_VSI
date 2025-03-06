hostname = ["BDP-CEN-01-BNG-005","BET-GUA-01-BNG-003","CEM-TLP-01-BNG-009","DVL-VSA-01-BNG-014","CPO-ANT-01-BNG-004","IRP-CAN-01-BNG-005","LPT-CEN-01-BNG-004","PDS-JARF-01-BNG-007","SDT-CEN-01-BNG-005"]




def menu ():

    host = int(input("""
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
                 
Selecione o local de autenticação: """))

    match host:
        case 1: #BOM DESPACHO#
            conc_primary = "BDP-CEN-01-BNG-005"
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
            conc_primary = "BET-GUA-01-BNG-003"
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
            conc_primary = "CEM-TLP-01-BNG-009"
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
            conc_primary = "DVL-VSA-01-BNG-014"
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
            conc_primary = "CPO-ANT-01-BNG-004"
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
            conc_primary = "IRP-CAN-01-BNG-005"
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
            conc_primary = "LPT-CEN-01-BNG-004"
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
            conc_primary = "PDS-JARF-01-BNG-007"
            interface_pppoe = "Eth-Trunk2"
            interface_type = "trunk"
            conc_secondary = "LPT-CEN-01-BNG-004"
            interface_pppoe_secondary = "Eth-Trunk2"
            interface_type_secondary = "trunk"
            conc_tertiary = "DVL-VSA-01-BNG-014"
            interface_pppoe_tertiary = "Eth-Trunk2"
            interface_type_tertiary = "hybrid"
            print(f"Você selecionou {hostname[7]}!")
        case 9: #SAMONTE#
            conc_primary = "SDT-CEN-01-BNG-005"
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
        
    return conc_primary, interface_pppoe, interface_type, conc_secondary, interface_pppoe_secondary, interface_type_secondary, conc_tertiary, interface_pppoe_tertiary, interface_type_tertiary
