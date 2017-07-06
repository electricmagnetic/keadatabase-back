from django.contrib.gis.db import models
from django.utils.text import slugify

SPECIFICITY_CHOICES = (
    ('general', 'Area (general)'),
    ('specific', 'Specific (point)'),
)

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


class Region(models.Model):
    """ Wider regions, designed to be made up of imported StudyArea objects """

    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, primary_key=True, editable=False)

    description = models.CharField(max_length=200, blank=True, null=True)

    study_areas = models.ManyToManyField(StudyArea)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """ Generate slug from name """

        self.slug = slugify(self.name)
        super(Region, self).save(*args, **kwargs)

class CommonLocation(models.Model):
    """ Point data (and specificity) for common locations where there might be birds """

    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, primary_key=True, editable=False)

    point_location = models.PointField()
    specificity = models.CharField(max_length=15, choices=SPECIFICITY_CHOICES, default='general')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """ Generate slug from name """

        self.slug = slugify(self.name)
        super(CommonLocation, self).save(*args, **kwargs)
