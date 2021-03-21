from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Ferma(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    host = models.CharField(max_length=250)
    port = models.IntegerField()

    def __str__(self):
        return f'{self.title}'

