from autoslug import AutoSlugField

from django.contrib.gis.db import models


# Models
class LocationBase(models.Model):
    """ Base abstract class for locations """
    class Meta:
        abstract = True


    # Fields
    ## Basic details
    name = models.CharField(max_length=200)

    ## Unique slug (for comparisons)
    slug = AutoSlugField(populate_from='name', unique=True, always_update=True)


    # Functions
    def __str__(self):
        return self.name


class PrimaryLocation(LocationBase):
    """ Primary location (wider regions) """
    # Fields
    mpoly = models.MultiPolygonField(null=True, blank=True)


class SecondaryLocation(LocationBase):
    """ Secondary location (more specific sub-regions) """
    # Fields
    primary_location = models.ForeignKey(PrimaryLocation, on_delete=models.CASCADE)


class AreaLocation(LocationBase):
    """ Main area, as designated by DOC Kea Database """
    # Fields
    mpoly = models.MultiPolygonField(null=True, blank=True)
