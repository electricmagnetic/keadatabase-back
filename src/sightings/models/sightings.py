""" Sightings models (contributor and media in other files) """

from django.contrib.gis.db import models
from versatileimagefield.fields import VersatileImageField

from locations.models import SPECIFICITY_CHOICES
from locations.models import Region
from .contributors import SightingsContributor

ACCURACY_CHOICES = (
    ('estimated', 'Estimated, used map'),
    ('known', 'Known, used map'),
    ('gps', 'GPS coordinates'),
)

VERIFICATION_CHOICES = (
    ('-1', '(-1) Unverified'),
    ('0', '(0) Bad'),
    ('1', '(1) OK'),
    ('2', '(2) Confirmed'),
)

SIGHTING_TYPE_CHOICES = (
    ('heard', 'Heard'),
    ('sighted', 'Sighted'),
)

class SightingsBase(models.Model):
    """ Sightings information common to sightings and non-sightings """

    contributor = models.OneToOneField(
        SightingsContributor,
        on_delete=models.PROTECT
    )

    date_sighted = models.DateField()
    time_sighted = models.TimeField()

    region = models.ForeignKey(Region, on_delete=models.PROTECT)

    # Optional
    comments = models.TextField(blank=True)

    # Staff only
    quality = models.CharField(max_length=3, choices=VERIFICATION_CHOICES, default='-1')

    # Metadata
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    ## TODO: Validate date_sighted is not from the future

    class Meta:
        abstract = True

class SightingsNonSighting(SightingsBase):
    """ Information specific to a non-sighting """
    location_details = models.TextField()

    # Optional
    expectations = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Non-sighting'
        ordering = ['-date_sighted', '-time_sighted',]

    def __str__(self):
        return "%s %s" % (self.date_sighted, self.time_sighted)

class SightingsSighting(SightingsBase):
    """ Information specific to a sighting """
    sighting_type = models.CharField(max_length=15, choices=SIGHTING_TYPE_CHOICES,
                                     default='sighted')

    point_location = models.PointField()
    accuracy = models.CharField(max_length=15, choices=ACCURACY_CHOICES, default='estimated')
    specificity = models.CharField(max_length=15, choices=SPECIFICITY_CHOICES, default='general')

    number = models.PositiveIntegerField()

    # Optional
    location_details = models.TextField(blank=True)
    behaviour = models.TextField(blank=True)

    ## TODO: Check number is greater than zero (should be an non-sighting otherwise)
    ## TODO: Check number is within bounds of New Zealand

    class Meta:
        verbose_name = 'Sighting'
        ordering = ['-date_sighted', '-time_sighted',]

    def __str__(self):
        return "%s %d on %s %s" % (self.get_sighting_type_display(), self.number, self.date_sighted, self.time_sighted)
