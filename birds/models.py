from datetime import date

from autoslug import AutoSlugField

from django.contrib.gis.db import models
from django.core.exceptions import ValidationError

from locations.models import AreaLocation
from sightings.models import Sighting
from bands.models import BandCombo
from keadatabase.choices import *


# Helper Functions
def bird_directory_path(instance, filename):
    return 'birds/%s/%s' % (instance.id, filename)


# Models
class Bird(models.Model):
    """ A model (intended to be read-only) imported from Access """
    # Fields
    ## Basic details
    name = models.CharField(max_length=200)
    sex = models.CharField(max_length=1, blank=True, choices=SEX_CHOICES, default='Undetermined')
    status = models.CharField(max_length=1, blank=True, choices=STATUS_CHOICES, default='A')
    birthday = models.DateField(blank=True, null=True)


    ## Unique slug (for comparisons)
    slug = AutoSlugField(populate_from='name', unique=True, always_update=True)


    ## Media
    photo = models.ImageField(upload_to=bird_directory_path, blank=True, null=True)


    ## Location details
    area = models.ForeignKey(AreaLocation, blank=True, null=True)


    ## Band details
    # TODO: band_combo = models.OneToOneField(BandCombo, null=True, blank=True)


    ## Metadata
    date_changed = models.DateTimeField(auto_now=True)
    date_imported = models.DateTimeField(blank=True, null=True)


    # Functions
    def __str__(self):
        return self.name


    def get_age(self):
        """ Calculates age based on birthday """
        ## Validate birthday is not from the future
        #     current_date = date.today()
        #     if self.birthday:
        #         if self.birthday > current_date:
        #             errors.update({'birthday': 'Date cannot be from the future.'})
        return 'age'


    def get_life_stage(self):
        """ Calculates life stage based on age """
        # choices=LIFE_STAGE_CHOICES
        return 'life stage'


class BirdExtended(models.Model):
    """ A complementary model to Bird, intended to be editable """
    bird = models.OneToOneField(Bird, models.CASCADE)
    featured = models.BooleanField(default=False)
    description = models.TextField()

    def __str__(self):
        return self.bird.__str__()


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
