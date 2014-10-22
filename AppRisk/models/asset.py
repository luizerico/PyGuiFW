from django.db import models
from django import forms
from django.contrib.admin import widgets
from AppRisk.models.risk import Risk

# Create your models here.

class Asset(models.Model):
    name = models.CharField(max_length=250)
    type = models.CharField(max_length=250)
    risk = models.ManyToManyField(Risk)
    register = models.DateField(null=True, default='1977-10-10')

    def __str__(self):
        return self.name


class AssetForm(forms.ModelForm):

    risk = forms.ModelMultipleChoiceField(Risk.objects.all(),
                                                   widget=widgets.FilteredSelectMultiple("Risk", False, attrs={}))

    class Meta:
        model = Asset
        widgets = {
            'register': widgets.AdminDateWidget()
        }
