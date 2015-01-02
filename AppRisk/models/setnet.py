from django.db import models
from django import forms
from AppRisk.models import setip

from AppRisk.models.network import Network

# Create your models here.

class Setnet(setip.Setip):
    address = models.ManyToManyField(Network, blank=True, related_name='setnet_address')

    @staticmethod
    def buildSet():
        list0 = ""
        for set in Setnet.objects.all():
            list0 = ','.join(item.getFullAddress() for item in set.address.all())

        return list0


class SetnetForm(forms.ModelForm):
    class Meta:
        model = Setnet