from django.db import models
from django import forms
from audit_log.models.managers import AuditLog

class Ipset(models.Model):
    name = models.CharField(max_length=250)
    #address = models.ManyToManyField(Address, blank=True, related_name='setip_address')

    #audit_log = AuditLog()

    def __str__(self):
        return self.name


class FormIpset(forms.ModelForm):
    class Meta:
        model = Ipset