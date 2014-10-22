from django.db import models
from django import forms
from django.contrib.admin import widgets

from AppRisk.models.host import Host
from AppRisk.models.network import Network
from AppRisk.models.url import URL
from AppRisk.models.interface import Interface
from AppRisk.models.port import Port
from AppRisk.models.protocol import Protocol


# Create your models here.


class Rule(models.Model):
    order = models.IntegerField()
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    source = models.ManyToManyField(Host, related_name='source')
    destin = models.ManyToManyField(Host, related_name='destin')
    port = models.ManyToManyField(Port)
    interface = models.ForeignKey(Interface)
    protocol = models.ManyToManyField(Protocol)

    #icon = models.ImageField(upload_to='images', blank=True)

    def __str__(self):
        return self.name