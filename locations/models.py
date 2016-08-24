from django.contrib.gis.db import models


# Models
class LocationBase(models.Model):
    """ Base abstract class for locations """

    class Meta:
        abstract = True


    # Fields
    name = models.CharField(max_length=200)


    # Functions
    def __str__(self):
        return self.name


class PrimaryLocation(LocationBase):
    """ Primary location (wider regions) """

    # Fields
    mpoly = models.MultiPolygonField(null=True, blank=True)


    # Functions
    # TODO tidy up and test
    #def get_secondary_locations(self):
    #    return ", ".join(str(secondary_location) for secondary_location in self.secondarylocation_set.all())


class SecondaryLocation(LocationBase):
    """ Secondary location (more specific sub-regions) """

    # Fields
    primary_location = models.ForeignKey(PrimaryLocation, on_delete=models.CASCADE)
