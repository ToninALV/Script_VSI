

def get_interface():
    interface = input("Qual a interface? ")
    speed_interface = input("Qual a modulação da Interface? (1G/10G/100G/eth) ")
    if speed_interface == "1":
        interface = f"GigabitEthernet 0/0/{interface}"
    elif speed_interface == "10":
        interface = f"XGigabitEthernet 0/0/{interface}"
    elif speed_interface == "100":
        interface = f"100GE 0/0/{interface}"
    elif speed_interface == "eth":
         interface = f"Eth-trunk{interface}"
    else:
        pass

    return interface

