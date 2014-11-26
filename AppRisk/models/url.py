from django import forms
from AppRisk.models import address

# Create your models here.


class URL(address.Address):
    pass


class FormURL(forms.ModelForm):

    class Meta:
        model = URL
        fields = ['name', 'address', 'description']