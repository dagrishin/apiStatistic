from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
# from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, HttpResponseRedirect
# from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, FormView
from django.views.generic.edit import UpdateView, DeleteView
# from django.views.generic.base import View
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .forms import CreateInformerForm
from .models import Informer, InformerData
from .utilites import get_inform_gpu, server_connect


def add_informer_data(informer_id, informer_data):
    date = timezone.now()
    for data in informer_data:
        obj = InformerData.objects.create(
            informer_id=informer_id,
            date=date,
            msg=data['msg'],
            enable=data['enabled'],
            temperature=float(data['temperature']),
            fan_speed=int(data['fan_speed']),
            fan_percent=int(data['fan_percent']),
            gpu_clock=int(data['gpu_clock']),
            memory_clock=int(data['memory_clock']),
            gpu_voltage=float(data['gpu_voltage']),
            gpu_activity=int(data['gpu_activity']),
            mhs=float(data['mhs']),
            mhs_30s=float(data['mhs_30s']),
            accepted=int(data['accepted']),
            rejected=int(data['rejected']),
            error=int(data['error']))
        print(obj)


class InformerGetMixin(object):

    def get(self, *args, **kwargs):
        informer_id = kwargs['pk']
        user_informer = None
        for inform in Informer.objects.filter(pk=informer_id):
            user_informer = inform.user.id
        if not user_informer or user_informer != self.request.user.id:
            messages.error(
                self.request,
                _(f'Вы не имеете права редактировать данный контент или контента не существует'))
            return HttpResponseRedirect('/')
        return super().get(self.request, *args, **kwargs)

    # def post(self, *args, **kwargs):
    #     informer_id = kwargs['pk']
    #     user_informer = None
    #     for inform in Informer.objects.filter(pk=informer_id):
    #         user_informer = inform.user.id
    #     if not user_informer or user_informer != self.request.user.id:
    #         messages.success(
    #             self.request,
    #             _(f'Вы не имеете права редактировать данный контент или контента не существует'))
    #         return HttpResponseRedirect('/')
    #     return super().get(self.request, *args, **kwargs)


class UserAuthMixin(UserPassesTestMixin):
    url_redirect = reverse_lazy('login')

    def test_func(self):
        return self.request.user.is_authenticated

    def handle_no_permission(self):
        return HttpResponseRedirect(self.url_redirect)


class UserCreateInformerMixin(LoginRequiredMixin, UserPassesTestMixin):
    url_redirect = reverse_lazy('login')

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return HttpResponseRedirect(self.url_redirect)


class InformerAllView(LoginRequiredMixin, ListView):
    model = Informer
    template_name = 'collector/informers.html'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        informers = Informer.objects.filter(user=self.request.user)
        informers_data = []
        for informer in informers:
            info_gpu = get_inform_gpu(host=informer.host, port=informer.port)

            if info_gpu:
                # add_informer_data(informer_id=informer.id, informer_data=info_gpu)
                title = informer.title
                data = {'info_gpu': info_gpu}
                data['title'] = title
                data['pk'] = informer.id
                informers_data.append(data)

        kwargs['informers_data'] = informers_data
        return kwargs
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class InformerDetailView(InformerGetMixin, LoginRequiredMixin, DetailView):
    model = Informer
    template_name = 'collector/informer_detail.html'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        informer = Informer.objects.filter(pk=self.kwargs.get('pk')).first()
        info_gpu = get_inform_gpu(host=informer.host, port=informer.port)

        if info_gpu:
            add_informer_data(informer_id=informer.id,
                              informer_data=info_gpu)
            title = informer.title
            data = {'info_gpu': info_gpu}
            data['title'] = title
            kwargs['data'] = data
        return kwargs


class CreateInformerView(LoginRequiredMixin, FormView):
    model = Informer
    template_name = 'collector/create_informer.html'
    success_url = reverse_lazy('informer:all')
    form_class = CreateInformerForm

    def form_valid(self, form):
        host = form.cleaned_data['host']
        port = form.cleaned_data['port']
        if server_connect(host, port):

            instance = Informer.objects.create(user=self.request.user,
                                               title=form.cleaned_data['title'],
                                               host=host,
                                               port=port, )

            messages.success(self.request, _(f'информер создан'))
            return super().form_valid(form)
        messages.error(self.request, _(f'Not connect'))
        return self.render_to_response(self.get_context_data(form=form))


    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))


class InformerUpdate(
    SuccessMessageMixin,
    InformerGetMixin,
    LoginRequiredMixin,
    UpdateView):
    """Обновление информера"""
    template_name = 'collector/create_informer.html'
    success_url = reverse_lazy('informer:all')
    model = Informer

    fields = ['title', 'host', 'port', 'timeout']
    success_message = _('информер изменен')

    #
    # def get_success_url(self):
    #     messages.success(self.request, self.success_message)
    #     return self.success_url.format(**self.object.__dict__)


class InformerDelete(LoginRequiredMixin, InformerGetMixin, DeleteView):
    """Класс удаления информера"""
    success_url = reverse_lazy('informer:all')
    template_name = 'collector/informer_confirm_delete.html'
    model = Informer

    def get_success_url(self):
        messages.success(self.request, _('Информер удален'))
        return self.success_url.format(**self.object.__dict__)
