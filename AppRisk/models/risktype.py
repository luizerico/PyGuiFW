from django.db import models
from django import forms
from django.contrib.admin import widgets

# Create your models here.


class RiskType(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()

    def __str__(self):
        return self.name
