from django.db import models

class Trafficclass(models.Model):
    name = models.CharField(max_length=250)
    flowid = models.IntegerField()
    rate = models.IntegerField()
    ceil = models.IntegerField(null=True, blank=True)
    burst = models.IntegerField(null=True, blank=True)
    prio = models.IntegerField(null=True, blank=True)
    perturb = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name