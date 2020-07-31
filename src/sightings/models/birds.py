""" Sightings related to a specific bird - must have a parent Sighting object """

from django.contrib.gis.db import models
from versatileimagefield.fields import VersatileImageField

from birds.models import SEX_CHOICES, LIFE_STAGE_CHOICES
from birds.models import Bird
from .observations import Sighting

BAND_CHOICES = (
    ('unknown', 'Couldn\'t tell'),
    ('unreadable', 'Banded, unreadable'),
    ('readable', 'Banded, readable'),
    ('unbanded', 'Not banded'),
)

SEX_CHOICES_UNSURE = (('', 'Unsure'),) + SEX_CHOICES
LIFE_STAGE_CHOICES_UNSURE = (('', 'Unsure'),) + LIFE_STAGE_CHOICES


class BirdSighting(models.Model):
    """ Information specific to a bird in a sighting """
    sighting = models.ForeignKey(Sighting, related_name='birds', on_delete=models.CASCADE)

    banded = models.CharField(max_length=15, choices=BAND_CHOICES)

    # Optional, depends on whether bird was banded or not
    band_combo = models.CharField(max_length=200, blank=True, null=True)
    sex_guess = models.CharField(max_length=15, choices=SEX_CHOICES_UNSURE, null=True, blank=True)
    life_stage_guess = models.CharField(max_length=15, choices=LIFE_STAGE_CHOICES_UNSURE,
                                        null=True, blank=True)

    # Staff only
    bird = models.ForeignKey(Bird, related_name='sightings', blank=True, null=True,
                             on_delete=models.SET_NULL)
    revisit = models.BooleanField(default=False, help_text='Moderator: tick if bird not added yet')

    class Meta:
        verbose_name = 'Bird sighting'

    def __str__(self):
        return "%s [%s]" % (self.id, self.sighting)
