# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-17 01:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('birds', '0004_auto_20161117_1133'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bird',
            name='banded_by',
        ),
        migrations.RemoveField(
            model_name='bird',
            name='caught_by',
        ),
        migrations.RemoveField(
            model_name='bird',
            name='caught_location',
        ),
        migrations.RemoveField(
            model_name='bird',
            name='date_caught',
        ),
    ]