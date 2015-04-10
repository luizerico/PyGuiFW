from django.db import models
from django import forms
from django.contrib.admin import widgets

from guifw.models.host import Host
from guifw.models.network import Network
from guifw.models.url import URL
from guifw.models.interface import Interface
from guifw.models.port import Port
from guifw.models.protocol import Protocol
from guifw.models.address import Address
from guifw.models.chain import Chain
from django.contrib.admin.widgets import FilteredSelectMultiple

# Create your models here.

class Nat(models.Model):
    ACTION = (('SNAT','Source NAT'),('DNAT','Destination NAT'),('MASQUERADE','Masquerade'))
    CONNECTION = ((0,'NEW'),(1, 'RELATED'),(2,'ESTABLISHED'),(3,'INVALID'),(4,'UNTRACKED'))
    LOG_LEVEL = (('debug','debug'),('info','info'),('notice','notice'),('warning','warning'),('error','error'),
                 ('crit','crit'),('alert','alert'),('emerg','emerg'))
    order = models.IntegerField()
    name = models.CharField(max_length=250)
    action = models.CharField(max_length=20, choices=ACTION, default='DNAT')
    source = models.ForeignKey(Address, blank=True, null=True, related_name='nat_source')
    srcport = models.ManyToManyField(Port, blank=True, related_name='nat_srcport')
    destiny = models.ForeignKey(Address, blank=True, null=True, related_name='nat_destiny')
    dstport = models.ManyToManyField(Port, blank=True, related_name='nat_dstport')
    protocol = models.ForeignKey(Protocol, null=True, blank=True)
    in_interface = models.ForeignKey(Interface, null=True, blank=True, related_name='nat_in_in')
    out_interface = models.ForeignKey(Interface, null=True, blank=True, related_name='nat_in_out')
    to_destiny = models.ForeignKey(Address, blank=True, null=True, related_name='to_destiny')
    to_port = models.ForeignKey(Port, blank=True, null=True, related_name='to_port')
    conn_state = models.CharField(max_length=150, null=True, blank=True)
    adv_options = models.CharField(max_length=250, blank=True, null=True)
    description = models.TextField(blank=True)
    log = models.BooleanField(default=False)
    log_level = models.CharField(max_length=20, choices=LOG_LEVEL, default='WARN')
    log_preffix = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class FormNat(forms.ModelForm):
    conn_state = forms.MultipleChoiceField(required=False,
                                           widget=forms.CheckboxSelectMultiple(),
                                           choices=Nat.CONNECTION)
    #source = forms.ModelMultipleChoiceField(Address.objects.all(), required=False,
    #                                        widget=FilteredSelectMultiple('Source', False,attrs={}))
    #destiny = forms.ModelMultipleChoiceField(Address.objects.all(), required=False,
    #                                        widget=FilteredSelectMultiple('Destiny', False,attrs={}))
    srcport = forms.ModelMultipleChoiceField(Port.objects.all(), required=False,
                                            widget=FilteredSelectMultiple('Source Port', False, attrs={}))
    dstport = forms.ModelMultipleChoiceField(Port.objects.all(), required=False,
                                            widget=FilteredSelectMultiple('Destiny Port', False, attrs={}))

    class Meta:
        model = Nat