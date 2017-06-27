# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-27 10:24
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bands', '0003_auto_20170621_1657'),
    ]

    operations = [
        migrations.AddField(
            model_name='bandcombo',
            name='colours',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), default=[], size=None),
        ),
        migrations.AddField(
            model_name='bandcombo',
            name='special',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='bandcombo',
            name='style',
            field=models.CharField(choices=[('old', 'Old'), ('new', 'New')], default='old', max_length=3),
        ),
        migrations.AddField(
            model_name='bandcombo',
            name='symbols',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), blank=True, default=[], size=None),
        ),
    ]
