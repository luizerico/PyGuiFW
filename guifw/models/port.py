from django.db import models
from django import forms
from audit_log.models.managers import AuditLog


# Create your models here.


class Port(models.Model):
    name = models.CharField(max_length=250)
    port = models.CharField(max_length=250)
    description = models.TextField(blank=True)

    audit_log = AuditLog()
    #icon = models.ImageField(upload_to='images', blank=True)

    def __str__(self):
        return self.name


class FormPort(forms.ModelForm):
    pass

    class Meta:
        model = Port