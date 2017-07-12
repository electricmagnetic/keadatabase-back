""" Sightings related to a specific bird - must have a parent SightingsSighting object """

from django.contrib.gis.db import models
from versatileimagefield.fields import VersatileImageField

from birds.models import SEX_CHOICES, LIFE_STAGE_CHOICES
from birds.models import Bird
from .sightings import SightingsSighting

BAND_CHOICES = (
    ('unknown', 'Couldn\'t tell'),
    ('unreadable', 'Banded, unreadable'),
    ('readable', 'Banded, readable'),
    ('unbanded', 'Not banded'),
)

class SightingsBird(models.Model):
    """ Information specific to a bird in a sighting """
    sighting = models.ForeignKey(SightingsSighting, related_name='birds')

    banded = models.CharField(max_length=15, choices=BAND_CHOICES, default='unknown')

    # Optional, depends on whether bird was banded or not
    band_combo = models.CharField(max_length=200, blank=True, null=True)
    sex_guess = models.CharField(max_length=15, choices=SEX_CHOICES, null=True, blank=True)
    life_stage_guess = models.CharField(max_length=15, choices=LIFE_STAGE_CHOICES,
                                        null=True, blank=True)

    # Staff only
    bird = models.ForeignKey(Bird, related_name='sightings', blank=True, null=True)

    class Meta:
        verbose_name = 'Bird sighting'
        ordering = ['banded',]

    def __str__(self):
        return "%s [%s]" % (self.id, self.sighting)
