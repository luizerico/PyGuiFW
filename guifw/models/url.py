from django import forms
from guifw.models import address
from audit_log.models.managers import AuditLog
# Create your models here.


class URL(address.Address):
    audit_log = AuditLog()
    pass


class FormURL(forms.ModelForm):

    class Meta:
        model = URL
        fields = ['name', 'address', 'description']