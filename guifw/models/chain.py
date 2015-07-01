from django.db import models
from django import forms

from audit_log.models.managers import AuditLog

# Create your models here.


class Chain(models.Model):
    ACTION = (('ACCEPT','ACCEPT'),('DROP','DROP'),('REJECT','REJECT'))
    name = models.CharField(max_length=250)
    default = models.CharField(max_length=20, choices=ACTION, default='DROP')
    description = models.TextField(blank=True)
    audit_log = AuditLog()

    def __str__(self):
        return self.name


class FormChain(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))

    class Meta:
        model = Chain