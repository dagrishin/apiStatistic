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

from .forms import CreateFermaForm
from .models import Ferma
from .utils import get_inform_gpu


class FermaGetMixin(object):

    def get(self, *args, **kwargs):
        ferma_id = kwargs['pk']
        for ferma in Ferma.objects.filter(pk=ferma_id):
            user = ferma.user.id
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


class UserCreateFermaMixin(LoginRequiredMixin, UserPassesTestMixin):
    url_redirect = reverse_lazy('login')

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return HttpResponseRedirect(self.url_redirect)


class FermaAllView(ListView):
    model = Ferma
    template_name = 'api/ferms.html'


class FermaDetailView(LoginRequiredMixin, DetailView):
    model = Ferma
    template_name = 'api/api_view.html'

    def get_context_data(self, **kwargs):
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

    def form_valid(self, form):
        instance = Ferma.objects.create(user=self.request.user,
                                        title=form.cleaned_data['title'],
                                        host=form.cleaned_data['host'],
                                        port=form.cleaned_data['port'], )

        messages.success(self.request, _(f'Датчик создан'))
        return super().form_valid(form)

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))


class FermaUpdate(
        SuccessMessageMixin,
        FermaGetMixin,
        LoginRequiredMixin,
        UpdateView):
    """Обновление фермы"""
    success_url = reverse_lazy('api:all')
    model = Ferma
    template_name = 'api/create_ferma.html'
    fields = ['title', 'host', 'port']
    success_message = _('Проукт изменен')


class FermaDelete(LoginRequiredMixin, FermaGetMixin, DeleteView):
    """Класс удаления фермы"""
    success_url = reverse_lazy('api:all')
    template_name = 'api/ferma_confirm_delete.html'
    model = Ferma

    def get_success_url(self):
        messages.success(self.request, _('Ферма удалена'))
        return self.success_url.format(**self.object.__dict__)
