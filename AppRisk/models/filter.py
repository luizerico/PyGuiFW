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
from AppRisk.models.action import Action
from AppRisk.models.chain import Chain
from AppRisk.models.loglevel import LogLevel

# Create your models here.

class Filter(models.Model):
    ACTION = (('ACCEPT','ACCEPT'),('DROP','DROP'),('REJECT','REJECT'))
    order = models.IntegerField()
    name = models.CharField(max_length=250)
    chain = models.ForeignKey(Chain)
    source = models.ManyToManyField(Address, blank=True, related_name='source')
    srcport = models.ManyToManyField(Port, blank=True, related_name='srcport')
    destiny = models.ManyToManyField(Address, blank=True, related_name='destiny')
    dstport = models.ManyToManyField(Port, blank=True, related_name='dstport')
    protocol = models.ForeignKey(Protocol, null=True, blank=True)
    in_interface = models.ForeignKey(Interface, null=True, blank=True, related_name='in_in')
    out_interface = models.ForeignKey(Interface, null=True, blank=True, related_name='in_out')
    #connection = models.ForeignKey(Connection, null=True, blank=True)
    conn_state = models.CharField(max_length=150, null=True, blank=True)
    adv_options = models.CharField(max_length=250, blank=True)
    action = models.CharField(max_length=20, choices=ACTION, default='DROP')
    description = models.TextField(blank=True)
    log = models.BooleanField(default=False)
    log_level = models.ForeignKey(LogLevel, null=True, blank=True, default=1)
    log_preffix = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class FilterForm(forms.ModelForm):
    CONNECTION = ((0,'NEW'),(1, 'RELATED'),(2,'ESTABLISHED'),(3,'INVALID'),(4,'UNTRACKED'))
    conn_state = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(),
                                      choices=CONNECTION)
    class Meta:
        model = Filter