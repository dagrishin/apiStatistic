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
    sock.send(b'summary')

    data = sock.recv(2048)
    sock.close()
    context = {'data': data}
    return render(request, 'api/api_view.html', context)

