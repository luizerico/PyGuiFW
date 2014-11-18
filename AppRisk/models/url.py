from django.db import models
from django import forms
from django.contrib.admin import widgets
from AppRisk.models import address

# Create your models here.


class URL(address.Address):
    address = models.CharField("URL", max_length=250)

    def __str__(self):
        return self.address