from django.db import models
from django import forms
from AppRisk.models import setip

from AppRisk.models.host import Host

# Create your models here.

class Sethost(setip.Setip):
    address = models.ManyToManyField(Host, blank=True, related_name='sethost_address')

    @staticmethod
    def buildSet():
        list0 = str(list(item for item in Sethost.objects.all()))
        return list0


class SethostForm(forms.ModelForm):
    class Meta:
        model = Sethost