from django.db import models

from birds.models import Bird
from locations.models import StudyArea

class BandCombo(models.Model):
    """ Basic band combo information, designed to be imported from Access """

    bird = models.OneToOneField(
        Bird,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='band_combo'
    )
    name = models.CharField(max_length=100, unique=True)

    study_area = models.ForeignKey(StudyArea)

    date_deployed = models.DateField()

    # Metadata
    date_modified = models.DateTimeField(auto_now=True)
    date_imported = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['bird']

    def __str__(self):
        return self.name
