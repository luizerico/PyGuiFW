from django.db import models
from django import forms
from django.contrib.admin import widgets
from AppRisk.models import address

# Create your models here.


class Host(address.Address):
    address = models.GenericIPAddressField(null=True)

    def __str__(self):
        return self.name
