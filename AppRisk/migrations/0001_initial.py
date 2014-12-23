# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=250)),
                ('description', models.TextField(blank=True)),
                ('address', models.CharField(default=b'', max_length=250)),
                ('mask', models.CharField(default=b'', max_length=250)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('address_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='AppRisk.Address')),
            ],
            options={
            },
            bases=('AppRisk.address',),
        ),
        migrations.CreateModel(
            name='Interface',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150)),
                ('device', models.CharField(max_length=150)),
                ('description', models.TextField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Network',
            fields=[
                ('address_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='AppRisk.Address')),
            ],
            options={
            },
            bases=('AppRisk.address',),
        ),
        migrations.CreateModel(
            name='Port',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('description', models.TextField(blank=True)),
                ('port', models.CharField(max_length=250)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Protocol',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('protocol', models.CharField(max_length=250)),
                ('description', models.TextField(blank=True)),
                ('number', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField()),
                ('name', models.CharField(max_length=250)),
                ('description', models.TextField(blank=True)),
                ('action', models.CharField(max_length=50, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='URL',
            fields=[
                ('address_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='AppRisk.Address')),
            ],
            options={
            },
            bases=('AppRisk.address',),
        ),
        migrations.AddField(
            model_name='rule',
            name='destiny',
            field=models.ManyToManyField(related_name=b'destiny', to='AppRisk.Address'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='rule',
            name='interface',
            field=models.ForeignKey(blank=True, to='AppRisk.Interface', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='rule',
            name='port',
            field=models.ManyToManyField(to='AppRisk.Port', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='rule',
            name='protocol',
            field=models.ManyToManyField(to='AppRisk.Protocol', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='rule',
            name='source',
            field=models.ManyToManyField(related_name=b'source', to='AppRisk.Address'),
            preserve_default=True,
        ),
    ]
