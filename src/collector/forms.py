from django import forms

from .models import Informer


class CreateInformerForm(forms.ModelForm):
    class Meta:
        model = Informer
        exclude = ['user']
