# Generated by Django 2.2.2 on 2019-06-17 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='surveyhour',
            old_name='status',
            new_name='activity',
        ),
        migrations.AddField(
            model_name='observer',
            name='purpose',
            field=models.CharField(blank=True, choices=[('', ''), ('tunnel', 'Tracking Tunnel Check'), ('fwf', 'FWF Hunting'), ('guide', 'Adventure Guiding'), ('trap', 'Pest Trapping'), ('permolat', 'Permolat/Remote Hut Work'), ('tramp', 'Tramping'), ('hunt', 'Hunting'), ('research', 'Researching'), ('other', 'Other')], default='', max_length=15),
        ),
    ]
