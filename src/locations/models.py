from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.text import slugify

GRIDTILE_LARGE_IMAGE_URL = "https://geo.keadatabase.nz/tiles/"
GRIDTILE_SMALL_IMAGE_URL = "https://geo.keadatabase.nz/small/"
GRIDTILE_IMAGE_TYPE = ".png"


class StudyArea(models.Model):
    """ Basic location information, designed to be imported from Access """

    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, primary_key=True, editable=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """ Generate slug from name """

        self.slug = slugify(self.name)
        super(StudyArea, self).save(*args, **kwargs)


class Place(models.Model):
    """ Place used to generate geocode strings """
    name_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    feat_type = models.CharField(max_length=200, blank=True, null=True)
    land_district = models.CharField(max_length=200, blank=True, null=True)

    point = models.PointField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Region(models.Model):
    """ Wider regions, designed to be made up of imported StudyArea objects """

    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, primary_key=True, editable=False)

    description = models.CharField(max_length=200, blank=True, null=True)

    study_areas = models.ManyToManyField(StudyArea)

    polygon = models.PolygonField(null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """ Generate slug from name """

        self.slug = slugify(self.name)
        super(Region, self).save(*args, **kwargs)


class GridTile(models.Model):
    """ Kea survey grid tile (5km by 5km) """
    id = models.CharField(primary_key=True, max_length=7)

    min = models.PointField(srid=2193)
    max = models.PointField(srid=2193)

    centroid = models.PointField(srid=4326)
    polygon = models.PolygonField(srid=4326)

    neighbours = ArrayField(models.CharField(max_length=7), size=8)

    def __str__(self):
        return self.id

    class Meta:
        ordering = ['id']

    def get_large_image(self):
        """ Return URL for large image """
        return (
            "%s%s%s" % (GRIDTILE_LARGE_IMAGE_URL, self.id, GRIDTILE_IMAGE_TYPE)
        )

    def get_small_image(self):
        """ Return URL for small image """
        return (
            "%s%s%s" % (GRIDTILE_SMALL_IMAGE_URL, self.id, GRIDTILE_IMAGE_TYPE)
        )
