from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View
import socket

def index_miner(request):


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
    context = []
    for gpu in range(count_gpu):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        command = f'gpu|{gpu}'
        sock.send(command.encode())
        data = sock.recv(1048).decode().split(',')
        sock.close()
        context.append({'temperature': data[7], data[8-9], ))
    return render(request, 'api/api_view.html', context)

