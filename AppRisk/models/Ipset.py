from django.db import models
from django import forms
from django.contrib.admin import widgets

from AppRisk.models.address import Address

# Create your models here.

class Ipset(models.Model):
    name = models.CharField(max_length=250)
    #address = models.ManyToManyField(Address, blank=True, related_name='setip_address')

    def __str__(self):
        return self.name


class FormIpset(forms.ModelForm):
    class Meta:
        model = Ipset