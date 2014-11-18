from django.db import models
from django import forms
from django.contrib.admin import widgets
from AppRisk.models import address

# Create your models here.

class Network(address.Address):
    address = models.GenericIPAddressField()
    mask = models.IPAddressField()

    def __str__(self):
        return self.name