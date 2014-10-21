# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AppRisk', '0002_remove_asset_register'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='register',
            field=models.DateField(default=b'1977-10-10', null=True),
            preserve_default=True,
        ),
    ]
