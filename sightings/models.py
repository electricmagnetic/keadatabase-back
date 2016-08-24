from django.contrib.gis.db import models

from locations.models import PrimaryLocation, SecondaryLocation


# Choices
CONTRIBUTOR_CHOICES = (
    ('', ''),
    ('TO', 'Tourist'),
    ('LO', 'Local'),
    ('SC', 'School group'),
    ('CG', 'Community group'),
    ('TR', 'Tramper'),
    ('HU', 'Hunter'),
    ('BI', 'Birder'),
    ('DO', 'DOC Staff'),
    ('OT', 'Other'),
)

ACCURACY_CHOICES = (
    ('', 'Unknown'),
    ('G', 'GPS coordinates'),
    ('E', 'Estimate from map'),
    ('O', 'Other'),
)


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
    newsletter = models.BooleanField()
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


    ## Birds details
    number_sighted = models.IntegerField(blank=True) # TODO verify is greater than zero


    ## Location details
    secondary_location = models.ForeignKey(SecondaryLocation, blank=True, null=True)
    point_location = models.PointField(null=True, blank=True)
    point_accuracy = models.CharField(max_length=1, blank=True, choices=ACCURACY_CHOICES,
                                      default='')


    ## Media
    # TODO photo(s)


    # Functions
    def __str__(self):
        return "%s, %s" % (self.date_sighted, self.primary_location)



#class NonSighting(SightingBase):
    #""" Information on non-sightings """
    #bar
