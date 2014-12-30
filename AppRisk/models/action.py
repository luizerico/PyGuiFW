from django.db import models
from django import forms
from django.contrib.admin import widgets

# Create your models here.


class Action(models.Model):
    action = models.CharField(max_length=250)
    #icon = models.ImageField(upload_to='images', blank=True)

    def __str__(self):
        return self.action