""" Sightings models (contributor and media in other files) """

from django.contrib.gis.db import models
from versatileimagefield.fields import VersatileImageField

from locations.models import Region
from .contributors import SightingsContributor

PRECISION_CHOICES = (
    (10, '(10m) GPS Coordinates'),
    (50, '(50m) Known Location'),
    (200, '(200m) Approximate Location'),
    (1000, '(1000m) General Area'),
)

VERIFICATION_CHOICES = (
    ('-1', '(-1) Unverified'),
    ('0', '(0) Bad'),
    ('1', '(1) OK'),
    ('2', '(2) Confirmed'),
)

SIGHTING_TYPE_CHOICES = (
    ('sighted', 'Sighted'),
    ('heard', 'Heard'),
    ('distant', 'Sighted (distant)'),
)

class SightingsBase(models.Model):
    """ Sightings information common to sightings and non-sightings """

    contributor = models.OneToOneField(
        SightingsContributor,
        on_delete=models.PROTECT
    )

    date_sighted = models.DateField()
    time_sighted = models.TimeField()

    region = models.ForeignKey(Region, on_delete=models.SET_NULL, blank=True, null=True)

    # Optional
    comments = models.TextField(blank=True)

    # Staff only
    quality = models.CharField(max_length=3, choices=VERIFICATION_CHOICES, default='-1',
                               help_text='Moderator: Select level of quality. \
                                          Confirmed should only be used for known contributors.')
    moderator_notes = models.TextField(blank=True,
                                       help_text='Moderator: Add notes here if you needed to \
                                                  change sighting information (not public).')

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
        return '%s %s' % (self.date_sighted, self.time_sighted)

class SightingsSighting(SightingsBase):
    """ Information specific to a sighting """
    sighting_type = models.CharField(max_length=15, choices=SIGHTING_TYPE_CHOICES)

    point_location = models.PointField()
    precision = models.PositiveIntegerField(choices=PRECISION_CHOICES)

    number = models.PositiveIntegerField()

    # Optional
    location_details = models.TextField(blank=True)
    behaviour = models.TextField(blank=True)

    # Staff only
    favourite = models.BooleanField(default=False, help_text="Moderator: If noteworthy sighting")

    # Automated
    geocode = models.CharField(max_length=200, blank=True, null=True)

    ## TODO: Check number is greater than zero (should be an non-sighting otherwise)
    ## TODO: Check number is within bounds of New Zealand

    class Meta:
        verbose_name = 'Sighting'
        ordering = ['-date_sighted', '-time_sighted',]

    def __str__(self):
        return '%s %d on %s %s' % (self.get_sighting_type_display(), self.number,
                                   self.date_sighted, self.time_sighted)
