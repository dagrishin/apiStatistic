from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View


class UserAuthMixin(UserPassesTestMixin):
    url_redirect = reverse_lazy('login')

    def test_func(self):
        return self.request.user.is_authenticated

    def handle_no_permission(self):
        return HttpResponseRedirect(self.url_redirect)

class IndexView(UserAuthMixin, View):
    url_redirect = reverse_lazy('informer:all')
    def get(self, *args, **kwargs):
        return HttpResponseRedirect(self.url_redirect)

