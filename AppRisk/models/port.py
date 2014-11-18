from django.db import models
from django import forms
from django.contrib.admin import widgets

# Create your models here.


class Port(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    port_from = models.IntegerField()
    port_to = models.IntegerField()
    #icon = models.ImageField(upload_to='images', blank=True)

    def __str__(self):
        return self.name