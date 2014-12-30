from django.db import models
from django import forms
from django.contrib.admin import widgets

# Create your models here.


class LogLevel(models.Model):
    name = models.CharField(max_length=100)
    number = models.IntegerField(default=0)
    #icon = models.ImageField(upload_to='images', blank=True)

    def __str__(self):
        return self.name
