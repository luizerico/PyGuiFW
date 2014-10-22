from django.db import models
from django import forms
from django.contrib.admin import widgets

# Create your models here.


class URL(models.Model):
    url = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    #icon = models.ImageField(upload_to='images', blank=True)

    def __str__(self):
        return self.url