from django.db import models
from guifw.models.interface import Interface
from audit_log.models.managers import AuditLog


class Shappclass(models.Model):
    name = models.CharField(max_length=250)
    parent = models.ForeignKey("self", blank=True, null=True)
    interface = models.ForeignKey(Interface, blank=True, null=True)
    flowid = models.IntegerField()
    rate = models.IntegerField()
    ceil = models.IntegerField(null=True, blank=True)
    burst = models.IntegerField(null=True, blank=True)
    prio = models.IntegerField(null=True, blank=True)
    perturb = models.IntegerField(null=True, blank=True)

    audit_log = AuditLog()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name