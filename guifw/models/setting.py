from django.db import models

class Setting(models.Model):
    readable_rules = models.BooleanField(default=True, verbose_name=u"Generate Readable Rules")
    restore_rules = models.BooleanField(default=True, verbose_name=u"Generate Restorable Rules")
    nat_rules = models.BooleanField(default=True, verbose_name=u"Generate Nat Rules")
    shapping_rules = models.BooleanField(default=True, verbose_name=u"Generate Shapping Rules")
    ipset_rules = models.BooleanField(default=True, verbose_name=u"Generate IPSet Rules")
    create_dns_cache = models.BooleanField(default=True, verbose_name=u"Create DNS Cache")
    save_path = models.CharField(max_length=250, blank=True)
    prerule = models.TextField(null=True, blank=True)
    postrule = models.TextField(null=True, blank=True)
