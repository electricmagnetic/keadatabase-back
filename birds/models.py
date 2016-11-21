from datetime import date

from django.contrib.gis.db import models
from django.core.exceptions import ValidationError

from locations.models import HomeLocation
from sightings.models import Sighting
from bands.models import BandCombo
from keadatabase.choices import *


# Helper Functions
def bird_directory_path(instance, filename):
    return 'birds/%s/%s' % (instance.id, filename)


# Models
class Bird(models.Model):
    """ Information on existing banded birds """
    # Fields
    ## Basic details
    name = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=1, blank=True, choices=STATUS_CHOICES, default='A')
    sex = models.CharField(max_length=1, blank=True, choices=SEX_CHOICES, default='')
    life_stage = models.CharField(max_length=1, blank=True, choices=LIFE_STAGE_CHOICES, default='')
    birthday = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)


    ## Media
    photo = models.ImageField(upload_to=bird_directory_path, blank=True, null=True)


    ## Location details
    home_location = models.ForeignKey(HomeLocation, blank=True, null=True)


    ## Band details
    band_combo = models.OneToOneField(BandCombo, null=True, blank=True)


    ## Notes
    health = models.TextField(blank=True)
    notes = models.TextField(blank=True)


    ## Metadata
    date_updated = models.DateTimeField(auto_now=True)


    # Functions
    def get_identifier(self):
        """ Creates string for identifying bird """
        if self.name:
            return self.name
        else:
            #return self.id_band
            return ''
    get_identifier.short_description = 'Identifier'


    """
    def get_colour_band(self):
         Passes 'get_colour_band' to Band
        if self.band:
            return self.band.get_colour_band()
        else:
            return ''
    get_colour_band.short_description = 'Colour band'
    """

    def __str__(self):
        return self.get_identifier()


    # Validation
    def clean(self):
        """ Validate various model fields to ensure uniqueness and consistency """
        errors = {}


        ## Validate birthday is not from the future
        current_date = date.today()
        if self.birthday:
            if self.birthday > current_date:
                errors.update({'birthday': 'Date cannot be from the future.'})


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
    # banded = models.CharField(max_length=1, blank=True, choices=BAND_CHOICES, default='N')
    #
    # band_style = models.CharField(max_length=1, blank=True, choices=BAND_STYLE_CHOICES,
    #                              verbose_name='Colour band type', default='')
    # band_colour = models.CharField(max_length=10, blank=True, choices=BAND_COLOUR_CHOICES,
    #                                default='')
    # band_symbol = models.CharField(max_length=1, blank=True)
    # band_symbol_colour = models.CharField(max_length=8, blank=True,
    #                                       choices=BAND_SYMBOL_COLOUR_CHOICES, default='')


    ## Verification details (admin only)
    verification = models.CharField(max_length=1, blank=True, choices=VERIFICATION_CHOICES,
                                    default='')


    ## Bird details (admin only)
    bird = models.ForeignKey(Bird, blank=True, null=True, related_name='sightings')
