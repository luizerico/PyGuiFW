from django.db import models
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from guifw.models import ipset
from guifw.models.network import Network
from audit_log.models.managers import AuditLog

class Netset(ipset.Ipset):
    address = models.ManyToManyField(Network, blank=True, related_name='netset_address')
    audit_log = AuditLog()

    @staticmethod
    def buildSet():
        list0 = ""
        for set in Netset.objects.all():
            list0 = ', '.join(item.getFullAddress() for item in set.address.all())

        return list0


class FormNetset(forms.ModelForm):
    address = forms.ModelMultipleChoiceField(Network.objects.all(), required=False,
                                            widget=FilteredSelectMultiple('Source', False,attrs={}))

    class Meta:
        model = Netset