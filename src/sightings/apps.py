from django.apps import AppConfig
from django.db.models.signals import pre_save

from .signals import run_geocode

class SightingsConfig(AppConfig):
    name = 'sightings'

    def ready(self):
        SightingsSighting = self.get_model('SightingsSighting')
        pre_save.connect(run_geocode, sender='sightings.SightingsSighting')
