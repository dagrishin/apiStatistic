from django import forms

from .models import Ferma


class CreateFermaForm(forms.ModelForm):
    class Meta:
        model = Ferma
        exclude = ['user']
