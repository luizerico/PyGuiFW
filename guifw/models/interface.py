from django.db import models
from django import forms
from guifw.library.sysnet import Sysnet
from audit_log.models.managers import AuditLog


class Interface(models.Model):
    name = models.CharField(max_length=150)
    device = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    #icon = models.ImageField(upload_to='images', blank=True)

    audit_log = AuditLog()

    def __str__(self):
        return self.name


class FormInterface(forms.ModelForm):
    inf = Sysnet()
    device = forms.ChoiceField(
        widget=forms.Select,
        choices=inf.allInterfaces(),
        # not worked
        #choices=(('1', '1'), ('2', '2')),  # worked
        #label='AAAA',
    )
    class Meta:
        model = Interface