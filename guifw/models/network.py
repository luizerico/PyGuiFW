from django import forms
from guifw.models import address
from audit_log.models.managers import AuditLog
# Create your models here.


class Network(address.Address):
    audit_log = AuditLog()
    pass


class FormNetwork(forms.ModelForm):
    address = forms.GenericIPAddressField()
    mask = forms.GenericIPAddressField()

    class Meta:
        model = Network
        fields = ['name', 'address', 'mask', 'description']