from address import Address
from django.db import models

class Trfclass(models.Model):
    name = models.CharField(max_length=250)
    classid = models.CharField()
    parent = models.ForeignKey(Traffic, blank=True, null=True)
    source = models.ForeignKey(Address, blank=False, null=False)
    destiny = models.ForeignKey(Address, blank=False, null=False)
    rate = models.IntegerField()
    ceil = models.IntegerField()
    burst = models.IntegerField()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name