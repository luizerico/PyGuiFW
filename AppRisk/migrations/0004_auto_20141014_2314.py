# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AppRisk', '0003_asset_register'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='name',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='asset',
            name='type',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='risk',
            name='name',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='risk',
            name='type',
            field=models.CharField(max_length=250),
        ),
    ]
