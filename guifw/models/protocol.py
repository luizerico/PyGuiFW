from django.db import models
from django import forms
from audit_log.models.managers import AuditLog

# Create your models here.


class Protocol(models.Model):
    name = models.CharField(max_length=250)
    number = models.IntegerField()
    description = models.TextField(blank=True)
    #icon = models.ImageField(upload_to='images', blank=True)
    audit_log = AuditLog()

    def __str__(self):
        return self.name


class FormProtocol(forms.ModelForm):

    class Meta:
        model = Protocol