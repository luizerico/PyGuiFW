from django.db import models
from django import forms
from django.contrib.admin import widgets

# Create your models here.


class Protocol(models.Model):
    protocol = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    number = models.IntegerField()
    #icon = models.ImageField(upload_to='images', blank=True)

    def __str__(self):
        return self.protocol