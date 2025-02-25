import paramiko


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
        print("*****CONEXÃO NÃO ESTABELECIDA*****")


    stdin, stdout, stderr = ssh.exec_command(command)
    stdout = stdout.read().decode('ascii').strip("\n")
    terminal = stdout
    terminal = str(stdout)

    ssh.close()


    return terminal