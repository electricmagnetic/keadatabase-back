from django.db import models
from django.contrib.postgres.fields import ArrayField

from birds.models import Bird
from locations.models import StudyArea

STYLE_CHOICES = (
    ('old', 'old'),
    ('new', 'new'),
)


class BandCombo(models.Model):
    """ Basic band combo information, designed to be imported from Access """

    bird = models.OneToOneField(
        Bird,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='band_combo'
    )
    name = models.CharField(max_length=100)
    style = models.CharField(max_length=3, choices=STYLE_CHOICES, default='old')
    special = models.CharField(max_length=100, blank=True, null=True)

    colours = ArrayField(models.CharField(max_length=50), default=list([]))
    symbols = ArrayField(models.CharField(max_length=50), blank=True, default=list([]))

    study_area = models.ForeignKey(StudyArea, on_delete=models.PROTECT)

    date_deployed = models.DateField()

    # Metadata
    date_modified = models.DateTimeField(auto_now=True)
    date_imported = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['bird']

    def __str__(self):
        return self.name
