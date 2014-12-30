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

class Nat(models.Model):
    ACTION = (('--snat','Source NAT'),('--dnat','Destination NAT'),('--masquerade','Masquerade'))
    order = models.IntegerField()
    name = models.CharField(max_length=250)
    action = models.CharField(max_length=20, choices=ACTION, default='DNAT')
    source = models.ForeignKey(Address, blank=True, null=True, related_name='nat_source')
    srcport = models.ForeignKey(Port, blank=True, null=True, related_name='nat_srcport')
    destiny = models.ForeignKey(Address, blank=True, null=True, related_name='nat_destiny')
    dstport = models.ForeignKey(Port, blank=True, null=True, related_name='nat_dstport')
    protocol = models.ForeignKey(Protocol, null=True, blank=True)
    in_interface = models.ForeignKey(Interface, null=True, blank=True, related_name='nat_in_in')
    out_interface = models.ForeignKey(Interface, null=True, blank=True, related_name='nat_in_out')
    to_destiny = models.ForeignKey(Address, blank=True, null=True, related_name='to_destiny')
    to_port = models.ForeignKey(Port, blank=True, null=True, related_name='to_port')
    adv_options = models.CharField(max_length=250, blank=True, null=True)
    description = models.TextField(blank=True)
    log = models.BooleanField(default=False)
    log_level = models.ForeignKey(LogLevel, null=True, blank=True, default=1)
    log_preffix = models.CharField(max_length=100, blank=True)


    def __str__(self):
        return self.name


class RuleForm(forms.Form):
    pass