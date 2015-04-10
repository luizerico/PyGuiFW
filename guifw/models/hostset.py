from django.db import models
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from guifw.models import Ipset
from guifw.models.host import Host

# Create your models here.

class Hostset(Ipset.Ipset):
    address = models.ManyToManyField(Host, blank=True, related_name='hostset_address')

    @staticmethod
    def buildSet():
        list0 = ""
        for set in Hostset.objects.all():
            list0 = ', '.join(item.getFullAddress() for item in set.address.all())

        return list0


class FormHostset(forms.ModelForm):
    address = forms.ModelMultipleChoiceField(Host.objects.all(), required=False,
                                            widget=FilteredSelectMultiple('Source', False,attrs={}))

    class Meta:
        model = Hostset