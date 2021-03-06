from django.db import models
from django.db.models import F
from django import forms
from guifw.models.address import Address
from guifw.models.port import Port
from guifw.models.shappclass import Shappclass
from audit_log.models.managers import AuditLog


class Shapping(models.Model):
    order = models.IntegerField()
    name = models.CharField(max_length=250)
    shappclass = models.ForeignKey(Shappclass, related_name="shapp_class", on_delete=models.PROTECT)
    parent = models.ForeignKey("self", blank=True, null=True, related_name="shapp_parent", on_delete=models.PROTECT)
    source = models.ForeignKey(Address, blank=True, null=True, related_name="shapp_source", on_delete=models.PROTECT)
    srcport = models.ForeignKey(Port, blank=True, null=True, related_name="shapp_srcport", on_delete=models.PROTECT)
    destiny = models.ForeignKey(Address, blank=True, null=True, related_name="shapp_destiny", on_delete=models.PROTECT)
    dstport = models.ForeignKey(Port, blank=True, null=True, related_name="shapp_dstport", on_delete=models.PROTECT)

    audit_log = AuditLog()

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name

    def save(self):
        if self.pk is not None:
            if Shapping.objects.filter(order=self.order):
                orig = Shapping.objects.get(pk=self.pk)
                if orig.order > self.order:
                    Shapping.objects.filter(order__lt=orig.order, order__gte=self.order).update(order=F('order') + 1)
                elif orig.order < self.order:
                    Shapping.objects.filter(order__lte=self.order, order__gte=orig.order).update(order=F('order') - 1)
        else:
            Shapping.objects.filter(order__gte=self.order).update(order=F('order') + 1)

        super(Shapping, self).save()

    def delete(self):
        Shapping.objects.filter(order__gte=self.order).update(order=F('order') - 1)
        print self.order
        super(Shapping, self).delete()


class ShappingForm(forms.ModelForm):
    class Meta:
        Model = Shapping
