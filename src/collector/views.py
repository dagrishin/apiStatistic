from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, FormView, UpdateView, DeleteView
from django.views.generic.base import View
from django.utils.translation import gettext_lazy as _

from .forms import CreateInformerForm
from .models import Informer
from .utilites import get_inform_gpu


class InformerGetMixin(object):

    def get(self, *args, **kwargs):
        informer_id = kwargs['pk']
        for inform in Informer.objects.filter(pk=informer_id):
            user = inform.user.id
        if user != self.request.user.id:
            messages.success(
                self.request,
                _(f'Вы не имеете права редактировать данный контент'))
            return HttpResponseRedirect('/')
        return super().get(self.request, *args, **kwargs)


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


class InformerAllView(ListView):
    model = Informer
    template_name = 'collector/informers.html'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class InformerDetailView(InformerGetMixin, LoginRequiredMixin, DetailView):
    model = Informer
    template_name = 'collector/collector_view.html'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        informer_data = Informer.objects.filter(pk=self.kwargs.get('pk')).first()
        info_gpu = get_inform_gpu(host=informer_data.host, port=informer_data.port)
        if info_gpu:
            kwargs['data'] = info_gpu
        return kwargs


class CreateInformerView(LoginRequiredMixin, FormView):
    model = Informer
    template_name = 'collector/create_informer.html'
    success_url = reverse_lazy('collector:all')
    form_class = CreateInformerForm

    def form_valid(self, form):
        instance = Informer.objects.create(user=self.request.user,
                                        title=form.cleaned_data['title'],
                                        host=form.cleaned_data['host'],
                                        port=form.cleaned_data['port'], )

        messages.success(self.request, _(f'информер создан'))
        return super().form_valid(form)

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))


class InformerUpdate(
        SuccessMessageMixin,
        InformerGetMixin,
        LoginRequiredMixin,
        UpdateView):
    """Обновление информера"""
    success_url = reverse_lazy('collector:all')
    model = Informer
    template_name = 'collector/create_informer.html'
    fields = ['title', 'host', 'port']
    success_message = _('информер изменен')


class InformerDelete(LoginRequiredMixin, InformerGetMixin, DeleteView):
    """Класс удаления информера"""
    success_url = reverse_lazy('collector:all')
    template_name = 'collector/informer_confirm_delete.html'
    model = Informer

    def get_success_url(self):
        messages.success(self.request, _('Информер удален'))
        return self.success_url.format(**self.object.__dict__)