from django.db import models


class Location(models.Model):
    """ Base abstract class for locations """

    name = models.CharField(max_length=200)

    class Meta: # pylint: disable=W0232,R0903,C1001
        abstract = True


class PrimaryLocation(Location):
    """ Primary location (wider regions) """

    class Meta: # pylint: disable=W0232,R0903,C1001
        abstract = False


class SecondaryLocation(Location):
    """ Secondary location (more specific sub-regions) """

    primary_location = models.ForeignKey(PrimaryLocation)
