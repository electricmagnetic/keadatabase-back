# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-17 01:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('birds', '0005_auto_20161117_1418'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bird',
            name='transmitter_channel',
        ),
    ]
