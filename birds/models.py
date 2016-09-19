from datetime import date

from django.contrib.gis.db import models
from django.core.exceptions import ValidationError


from locations.models import PrimaryLocation, SecondaryLocation
from sightings.models import Sighting
from bands.models import Band
from bands.models import BAND_TYPE_CHOICES, BAND_COLOUR_CHOICES, BAND_SYMBOL_COLOUR_CHOICES


# Choices
BAND_CHOICES = (
    ('', 'Couldn\'t tell'),
    ('U', 'Banded, unreadable'),
    ('B', 'Banded, readable'),
    ('N', 'Not banded'),
)

VERIFICATION_CHOICES = (
    ('', 'Unverified'),
    ('Q', 'Questionable'),
    ('G', 'Good'),
    ('C', 'Confirmed'),
)

SEX_CHOICES = (
    ('', 'Unknown'),
    ('F', 'Female'),
    ('M', 'Male'),
)

LIFE_STAGE_CHOICES = (
    ('', 'Unknown'),
    ('A', 'Adult'),
    ('S', 'Sub-adult'),
    ('J', 'Juvenile'),
    ('F', 'Fledgling'),
)

STATUS_CHOICES = (
    ('A', 'Alive'),
    ('D', 'Dead'),
)


# Models
class Bird(models.Model):
    """ Information on existing banded birds """
    # Fields
    ## Basic details
    name = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=1, blank=True, choices=STATUS_CHOICES, default='A')
    sex = models.CharField(max_length=1, blank=True, choices=SEX_CHOICES, default='')
    life_stage = models.CharField(max_length=1, blank=True, choices=LIFE_STAGE_CHOICES, default='')
    age = models.IntegerField(blank=True, null=True, verbose_name='Approximate age (years)')
    family = models.CharField(max_length=200, blank=True)


    ## Location details
    primary_location = models.ForeignKey(PrimaryLocation, blank=True, null=True)
    secondary_location = models.ForeignKey(SecondaryLocation, blank=True, null=True)


    ## Catch details
    date_caught = models.DateField(blank=True, null=True)

    caught_by = models.CharField(max_length=200, blank=True)
    banded_by = models.CharField(max_length=200, blank=True)

    caught_location = models.PointField(null=True, blank=True)


    ## Band details
    band = models.OneToOneField(Band)


    ## Transmitter details
    transmitter_channel = models.CharField(max_length=10, blank=True)


    ## Notes
    health = models.TextField(blank=True)
    notes = models.TextField(blank=True)


    ## Media
    # TODO photo


    ## Metadata
    date_updated = models.DateTimeField(auto_now=True)


    # Functions
    def get_identifier(self):
        """ Creates string for identifying bird """
        if self.name:
            return self.name
        else:
            return str(self.band)
    get_identifier.short_description = 'Identifier'


    def get_location(self):
        """ Creates string for location """
        if self.primary_location and self.secondary_location:
            return '%s (%s)' % (self.primary_location, self.secondary_location)
        elif self.primary_location:
            return '%s' % (self.primary_location)
        else:
            return ''
    get_location.short_description = 'Location'


    def get_id_band(self):
        """ Passes 'get_id_band' to Band """
        return self.band.get_id_band()
    get_id_band.short_description = 'ID band'


    def get_colour_band(self):
        """ Passes 'get_colour_band' to Band """
        return self.band.get_colour_band()
    get_colour_band.short_description = 'Colour band'


    def __str__(self):
        return self.get_identifier()


    # Validation
    def clean(self):
        """ Validate various model fields to ensure uniqueness and consistency """
        errors = {}

        ## Validate date_caught is not from the future
        current_date = date.today()
        if self.date_caught:
            if self.date_caught > current_date:
                errors.update({'date_caught': 'Date cannot be from the future.'})


        ## Validate secondary_location is paired with/is a child of primary_location
        if self.primary_location and self.secondary_location:
            if self.secondary_location.primary_location != self.primary_location:
                errors.update({'secondary_location': 'Secondary location must be in ' \
                                                              'primary location.'})
        elif self.secondary_location:
            errors.update({'primary_location': 'Must have primary location if secondary ' \
                                                        'location is specified.'})

        ## If any errors occur, raise them
        if errors:
            raise ValidationError(errors)


class BirdSighting(models.Model):
    """ Foreign key of Sighting, able to be verified and tagged to a particular Bird """
    # Fields
    ## Foreign key
    sighting = models.ForeignKey(Sighting, related_name='birds')


    ## Basic details
    status = models.CharField(max_length=1, blank=True, choices=STATUS_CHOICES, default='A')
    sex = models.CharField(max_length=1, blank=True, choices=SEX_CHOICES, default='')
    life_stage = models.CharField(max_length=1, blank=True, choices=LIFE_STAGE_CHOICES, default='')


    ## Band details
    banded = models.CharField(max_length=1, blank=True, choices=BAND_CHOICES, default='N')

    colour_band_type = models.CharField(max_length=1, blank=True, choices=BAND_TYPE_CHOICES,
                                        verbose_name='Colour band type', default='')
    colour_band_colour = models.CharField(max_length=8, blank=True, choices=BAND_COLOUR_CHOICES,
                                          default='')
    colour_band_symbol = models.CharField(max_length=1, blank=True)
    colour_band_symbol_colour = models.CharField(max_length=8, blank=True,
                                                 choices=BAND_SYMBOL_COLOUR_CHOICES, default='')


    ## Verification details (admin only)
    verification = models.CharField(max_length=1, blank=True, choices=VERIFICATION_CHOICES,
                                    default='')


    ## Bird details (admin only)
    bird = models.ForeignKey(Bird, blank=True, null=True, related_name='sightings')
