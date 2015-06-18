from django import forms
from guifw.models import address
from audit_log.models.managers import AuditLog

# Create your models here.


class Host(address.Address):
    audit_log = AuditLog()
    pass


class FormHost(forms.ModelForm):
    address = forms.GenericIPAddressField()

    class Meta:
        model = Host
        fields = ['name', 'address', 'description']
