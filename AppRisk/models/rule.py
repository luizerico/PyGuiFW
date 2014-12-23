from django.db import models
from django import forms
from django.contrib.admin import widgets

from AppRisk.models.host import Host
from AppRisk.models.network import Network
from AppRisk.models.url import URL
from AppRisk.models.interface import Interface
from AppRisk.models.port import Port
from AppRisk.models.protocol import Protocol
from AppRisk.models.address import Address

# Create your models here.

class Rule(models.Model):
    order = models.IntegerField()
    name = models.CharField(max_length=250)
    source = models.ManyToManyField(Address, related_name='source', blank=True)
    srcport = models.ManyToManyField(Port, blank=True, related_name='srcport')
    destiny = models.ManyToManyField(Address, related_name='destiny', blank=True)
    dstport = models.ManyToManyField(Port, blank=True, related_name='dstport')
    protocol = models.ForeignKey(Protocol, null=True, blank=True)
    interface = models.ForeignKey(Interface, null=True, blank=True)
    action = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class RuleForm(forms.Form):
    pass