import paramiko


ssh =  paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('endereco_do_servidor', username='usuario', password='senha')


stdin, stdout, stderr = ssh.exec_command('ls')
print(stdout.read().decode('utf-8'))