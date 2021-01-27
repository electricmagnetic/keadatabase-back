from django.apps import AppConfig
from django.db.models.signals import pre_save

from .signals import run_geocode


class ObservationsConfig(AppConfig):
    name = 'sightings'

    def ready(self):
        Sighting = self.get_model('Sighting')
        pre_save.connect(run_geocode, sender='sightings.Sighting')
