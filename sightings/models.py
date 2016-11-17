from datetime import date

from django.contrib.gis.db import models
from django.core.exceptions import ValidationError

from keadatabase.choices import *
from locations.models import PrimaryLocation, SecondaryLocation


# Models
class SightingBase(models.Model):
    """ Base abstract class for sightings """
    class Meta:
        abstract = True


    # Fields
    ## Location details
    primary_location = models.ForeignKey(PrimaryLocation, blank=True, null=True)
    location_description = models.TextField(blank=True)


    ## Notes
    notes = models.TextField(blank=True)


    ## Contributor details
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=200, blank=True)
    email = models.EmailField(max_length=200)
    newsletter = models.BooleanField(default=False)
    category = models.CharField(max_length=2, blank=True, choices=CONTRIBUTOR_CHOICES, default='')


    ## Metadata
    date_updated = models.DateTimeField(auto_now=True)


class Sighting(SightingBase):
    """ Information on actual sightings, associated with BirdSighting """
    # Fields
    ## Basic details
    date_sighted = models.DateField()
    time_sighted = models.TimeField()
    # TODO sighting_type


    ## Location details
    secondary_location = models.ForeignKey(SecondaryLocation, blank=True, null=True)
    point_location = models.PointField(null=True, blank=True)
    point_accuracy = models.CharField(max_length=1, blank=True, choices=ACCURACY_CHOICES,
                                      default='')


    ## Media
    # TODO photo(s)


    # Functions
    def __str__(self):
        return "%s in %s" % (self.date_sighted, self.primary_location)


    # Validation
    def clean(self):
        """ Validate various model fields to ensure uniqueness and consistency """
        errors = {}

        ## Validate date_sighted is not from the future
        current_date = date.today()
        if self.date_sighted:
            if self.date_sighted > current_date:
                errors.update({'date_sighted': 'Date cannot be from the future.'})


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


#class NonSighting(SightingBase):
    #""" Information on non-sightings """
