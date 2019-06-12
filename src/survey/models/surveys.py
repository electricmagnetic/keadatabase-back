from django.db import models

from .observers import Observer
from locations.models import GridTile

STATUS_CHOICES = (
    ('W', 'W - Walking'),
    ('S', 'S - Stationary'),
    ('C', 'C - At camp (tent)'),
    ('H', 'H - At human structure (hut, carpark)'),
    ('X', 'X - Not surveying'),
)

class Survey(models.Model):
    date = models.DateField()

    observer = models.OneToOneField(
        Observer,
        on_delete=models.PROTECT
    )

    comments = models.TextField()
    max_flock_size = models.PositiveIntegerField(null=True, blank=True)

    # TODO: geocoding?
    # TODO: moderation?
    # TODO: validate max flock size if child object has kea sighted?

    # Metadata
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return ("%s" % (self.id))

class SurveyHour(models.Model):
    survey = models.ForeignKey(Survey, related_name='hours', on_delete=models.CASCADE)
    hour = models.PositiveIntegerField()
    kea = models.BooleanField(default=False)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='')
    grid_tile = models.ForeignKey(GridTile, related_name='hours', on_delete=models.PROTECT)

    # TODO: error check ensuring unique hours only?

    def __str__(self):
        return ("At %i:00 in %s for survey #%s" % (self.hour, self.grid_tile, self.survey))
