from address import Address
from port import Port
from django.db import models
from guifw.models.trafficclass import Trafficclass

class Traffic(models.Model):
    name = models.CharField(max_length=250)
    trafficclass = models.ForeignKey(Trafficclass)
    parent = models.ForeignKey("self", blank=True, null=True)
    source = models.ForeignKey(Address, blank=True, null=True, related_name="tsource")
    srcport = models.ForeignKey(Port, blank=True, null=True, related_name="tsrc_port")
    destiny = models.ForeignKey(Address, blank=True, null=True, related_name="tdestiny")
    dstport = models.ForeignKey(Port, blank=True, null=True, related_name="tdst_port")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name