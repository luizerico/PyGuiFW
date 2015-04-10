from django import forms
from guifw.models import address

# Create your models here.


class Network(address.Address):
    pass


class FormNetwork(forms.ModelForm):
    address = forms.GenericIPAddressField()
    mask = forms.GenericIPAddressField()

    class Meta:
        model = Network
        fields = ['name', 'address', 'mask', 'description']