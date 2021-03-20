import socket
from pprint import pprint

host = 'abrep.ddns.net'
user = 'evgbog'
secret = 'Vilopand3'
port = 26541

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))
# count gpu
sock.send(b'config')
count_gpu = int(sock.recv(1048).decode().split(',')[5].split('=')[1])
print(count_gpu)
sock.close()
for gpu in range(count_gpu):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    command = f'gpu|{gpu}'
    print(command)
    # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # sock.connect((host, port))
    sock.send(command.encode())
    pprint(sock.recv(1048).decode().split(','))
    sock.close()


# context = {'data': data}
# data = data.
# pprint(data.decode().split(','))
