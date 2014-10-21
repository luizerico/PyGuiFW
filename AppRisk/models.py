from django.db import models
from django import forms
from django.contrib.admin import widgets

# Create your models here.


class RiskType(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()

    def __str__(self):
        return self.name


class Risk(models.Model):
    name = models.CharField(max_length=250)
    type = models.CharField(max_length=250)
    risktype = models.ForeignKey(RiskType, null=True)

    def __str__(self):
        return self.name


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





