from django.contrib.gis.db import models


class Location(models.Model):
    """ Base abstract class for locations """

    name = models.CharField(max_length=200)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class PrimaryLocation(Location):
    """ Primary location (wider regions) """

    mpoly = models.MultiPolygonField(null=True, blank=True)

    # TODO tidy up and test
    #def get_secondary_locations(self):
    #    return ", ".join(str(secondary_location) for secondary_location in self.secondarylocation_set.all())


class SecondaryLocation(Location):
    """ Secondary location (more specific sub-regions) """

    primary_location = models.ForeignKey(PrimaryLocation, on_delete=models.CASCADE)
