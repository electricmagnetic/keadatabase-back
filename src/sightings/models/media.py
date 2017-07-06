""" Media models for Sightings (sightings and non-sightings in .sightings)"""

from django.db import models
from versatileimagefield.fields import VersatileImageField

from sightings.models.sightings import SightingsSighting

def sighting_directory_path(instance, filename):
    """ Helper function for determining upload location for each sighting """
    return 'sighting/%s/%s' % (instance.sighting.id, filename)

class SightingsMedia(models.Model):
    """ User uploaded media for a sighting """
    sighting = models.ForeignKey(SightingsSighting, related_name='media')
    image = VersatileImageField(upload_to=sighting_directory_path)

    # Optional
    caption = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'media'
        verbose_name_plural = 'media'

    def __str__(self):
        return "%s [%s]" % (self.id, self.sighting)
