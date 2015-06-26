from django.db import models

class Setting(models.Model):
    readable_rules = models.BooleanField(default=True)
    restore_rules = models.BooleanField(default=True)
    save_path = models.CharField(max_length=250, blank=True)
    create_dns_cache = models.BooleanField(default=True)
    prerule = models.TextField(null=True, blank=True)
    postrule = models.TextField(null=True, blank=True)
