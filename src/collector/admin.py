from django.contrib import admin

# Register your models here.
from .models import Informer, InformerData

admin.site.register(Informer)
admin.site.register(InformerData)
