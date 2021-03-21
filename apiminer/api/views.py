from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, FormView
from django.views.generic.base import View
from django.utils.translation import gettext_lazy as _
import socket

from .forms import CreateFermaForm
from .models import Ferma


def get_inform_gpu(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    # count gpu
    sock.send(b'config')
    count_gpu = int(sock.recv(1048).decode().split(',')[5].split('=')[1])
    print(count_gpu)
    sock.close()
    data_list = []
    for gpu in range(count_gpu):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        command = f'gpu|{gpu}'
        sock.send(command.encode())
        data = sock.recv(1048).decode().split(',')
        sock.close()

        gpu_dict = {
            'Msg': data[3],
            'Enabled': data[5],
            'Temperature': data[7],
            'Fan_Speed': data[8],
            'Fan_Percent': data[9],
            'GPU_Clock': data[10],
            'Memory_Clock': data[11],
            'GPU_Voltage': data[12],
            'GPU_Activity': data[13],
            'MHS': data[15],
            'MHS_30s': data[16],
            'Accepted': data[19],
            'Rejected': data[20],
            'Hardware_Errors': data[21],
        }
        data_list.append(gpu_dict)
    return data_list

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
    data_list = []
    for gpu in range(count_gpu):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        command = f'gpu|{gpu}'
        sock.send(command.encode())
        data = sock.recv(1048).decode().split(',')
        sock.close()

        gpu_dict = {
            'Msg': data[3],
            'Enabled': data[5],
            'Temperature': data[7],
            'Fan_Speed': data[8],
            'Fan_Percent': data[9],
            'GPU_Clock': data[10],
            'Memory_Clock': data[11],
            'GPU_Voltage': data[12],
            'GPU_Activity': data[13],
            'MHS': data[15],
            'MHS_30s': data[16],
            'Accepted': data[19],
            'Rejected': data[20],
            'Hardware_Errors': data[21],
        }
        data_list.append(gpu_dict)
    return render(request, 'api/api_view.html', {'data': data_list})


class UserAuthMixin(UserPassesTestMixin):
    url_redirect = reverse_lazy('login')

    def test_func(self):
        return self.request.user.is_authenticated

    def handle_no_permission(self):
        return HttpResponseRedirect(self.url_redirect)

class UserCreateFermaMixin(LoginRequiredMixin, UserPassesTestMixin):
    url_redirect = reverse_lazy('login')

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return HttpResponseRedirect(self.url_redirect)


class FermaAllView(ListView):
    model = Ferma
    template_name = 'api/ferms.html'


# class FermaAdd(UserCreateFermaMixin, CreateView):
#     model = Ferma
#     form_class = CreateFermaForm
#     template_name = 'api/create_ferma.html'
#     success_url = reverse_lazy('all')


class FermaDetailView(LoginRequiredMixin, DetailView):
    model = Ferma
    template_name = 'api/api_view.html'

    def get_context_data(self, **kwargs):
        host = 'abrep.ddns.net'
        user = 'evgbog'
        secret = 'Vilopand3'
        port = 26541
        kwargs = super().get_context_data(**kwargs)
        ferma_data = Ferma.objects.filter(pk=self.kwargs.get('pk')).first()

        info_gpu = get_inform_gpu(host=ferma_data.host, port=ferma_data.port)
        kwargs['data'] = info_gpu
        return kwargs



class CreateFermaView(LoginRequiredMixin, FormView):
    model = Ferma
    template_name = 'api/create_ferma.html'
    success_url = reverse_lazy('api:all')
    form_class = CreateFermaForm
    # fields = ('title', 'participants')

    def form_valid(self, form):
        instance = Ferma.objects.create(user=self.request.user,
                                        title=form.cleaned_data['title'],
                                        host=form.cleaned_data['host'],
                                        port=form.cleaned_data['port'],)

        messages.success(self.request, _(f'Датчик создан'))
        return super().form_valid(form)
    # def form_invalid(self, form):
    #     print(form)

    def form_invalid(self, form):
        print('EEEEEEEEEEEEEEEEEEEEEEEEEEEE', form)
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))

    # def get_context_data(self, **kwargs):
    #     kwargs = super().get_context_data(**kwargs)
    #     friends = []
    #     contact = Contact.objects.get(user=self.request.user)
    #     for friend in contact.friends.all():
    #         friends.append(friend)
    #     form = self.form_class()
    #     form.fields["participants"].queryset = Contact.objects.filter(user__in=friends)
    #     kwargs['form'] = form
    #     return kwargs
