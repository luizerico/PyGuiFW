from django.db import models
from audit_log.models.fields import LastUserField
from audit_log.models.managers import AuditLog

# Create your models here.

class Address(models.Model):
    name = models.CharField(max_length=150, default="")
    description = models.CharField(max_length=300, null=True, blank=True)
    address = models.CharField(max_length=250, default="")
    mask = models.CharField(max_length=250, default="")

    audit_log = AuditLog()

    def __str__(self):
        return self.name

    def getFullAddress(self):
        if(self.mask):
            return self.address + "/" + self.mask
        else:
            return self.address