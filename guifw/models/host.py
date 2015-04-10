from django import forms
from guifw.models import address

# Create your models here.


class Host(address.Address):
    pass


class FormHost(forms.ModelForm):
    address = forms.GenericIPAddressField()

    class Meta:
        model = Host
        fields = ['name', 'address', 'description']
