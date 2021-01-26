# Generated by Django 3.0.11 on 2021-01-21 04:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sightings', '0035_auto_20200319_0753'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SightingImportReport',
        ),
        migrations.CreateModel(
            name='ObservationImportReport',
            fields=[
            ],
            options={
                'verbose_name': 'Import report',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('sightings.sighting',),
        ),
    ]
