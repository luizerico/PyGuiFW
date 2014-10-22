from django.db import models
from django import forms
from django.contrib.admin import widgets
from AppRisk.models.risktype import RiskType

# Create your models here.


class Risk(models.Model):
    name = models.CharField(max_length=250)
    type = models.CharField(max_length=250)
    risktype = models.ForeignKey(RiskType, null=True)

    def __str__(self):
        return self.name