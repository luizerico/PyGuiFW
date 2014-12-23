from django.db import models
from django import forms
from django.contrib.admin import widgets

# Create your models here.


class Address(models.Model):
    name = models.CharField(max_length=250, default="")
    description = models.TextField(blank=True)
    address = models.CharField(max_length=250, default="")
    mask = models.CharField(max_length=250, default="")
    # icon

    def __str__(self):
        return self.name

    def getFullAddress(self):
        if(self.mask):
            return self.address + "/" + self.mask
        else:
            return self.address