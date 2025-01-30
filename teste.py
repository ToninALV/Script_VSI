import paramiko


def connect_equipament():
    host = "10.128.44.3"
    port = "6422"
    username = "antonio.silva"
    password = "An@13606973659"
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port=port, username=username, password=password)
        print("----- TRABALHANDO -----")
    except:
        print("*****CONEXÃO NÃO ESTABELECIDA*****")

    print("estou aqui 1")
    stdin, stdout, stderr = ssh.exec_command(f"""display version\n""")
    terminal = stdout.read().decode('ascii').strip("\n")
    terminal = str(terminal)

    print(terminal)

    """stdout.read()
    terminal = stdout
    terminal = str(stdout)
    print(terminal)

    ssh.close()"""







connect_equipament()