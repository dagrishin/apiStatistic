from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Informer(models.Model):
    TIME_OUT_CHOICES = [
        (0.5, 0.5),
        (1, 1),
        (5, 5),
        (10, 10),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    host = models.CharField(max_length=250)
    port = models.IntegerField()
    timeout = models.IntegerField(choices=TIME_OUT_CHOICES, default=1)

    def __str__(self):
        return f'{self.title}'


class InformerData(models.Model):
    informer = models.ForeignKey(Informer, on_delete=models.CASCADE)
    date = models.DateTimeField()
    msg = models.CharField(max_length=100)
    enable = models.CharField(max_length=100)
    temperature = models.FloatField()
    fan_speed = models.IntegerField()
    fan_percent = models.IntegerField()
    gpu_clock = models.IntegerField()
    memory_clock = models.IntegerField()
    gpu_voltage = models.FloatField()
    gpu_activity = models.IntegerField()
    mhs = models.FloatField()
    mhs_30s = models.FloatField()
    accepted = models.IntegerField()
    rejected = models.IntegerField()
    error = models.IntegerField()

    def __str__(self):
        return f'{self.informer.title}'


