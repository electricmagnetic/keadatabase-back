from django.db import models
from django.core.exceptions import ValidationError

from .observers import Observer
from .choices import PURPOSE_CHOICES
from locations.models import GridTile

ACTIVITY_CHOICES = (
    ('W', 'W - Walking'),
    ('S', 'S - Stationary'),
    ('C', 'C - At camp (tent)'),
    ('H', 'H - At human structure (hut, carpark)'),
    ('X', 'X - Not surveying'),
)

STATUS_CHOICES = (
    ('new', 'New'),
    ('public', 'Verified (Public)'),
)

class Survey(models.Model):
    date = models.DateField()

    observer = models.OneToOneField(
        Observer,
        on_delete=models.PROTECT
    )

    purpose = models.CharField(max_length=15, blank=True, choices=PURPOSE_CHOICES, default='')
    comments = models.TextField(blank=True)
    max_flock_size = models.PositiveIntegerField(null=True, blank=True)

    # TODO: validate max flock size if child object has kea sighted?

    # Staff only
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')

    # Metadata
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return ("%s" % (self.id))

    class Meta:
        ordering = ['-date']

class SurveyHour(models.Model):
    survey = models.ForeignKey(Survey, related_name='hours', on_delete=models.CASCADE)
    hour = models.PositiveIntegerField()
    kea = models.BooleanField(default=False)
    activity = models.CharField(max_length=1, choices=ACTIVITY_CHOICES, default='')
    grid_tile = models.ForeignKey(GridTile, related_name='hours', on_delete=models.PROTECT,
                                  blank=True, null=True)

    class Meta:
        ordering = ['survey', 'hour']

    def __str__(self):
        return ("At %i:00 in %s for survey #%s" % (self.hour, self.grid_tile, self.survey))

    def get_hour_display(self):
        """ Better display of hour value """
        return ("%d:00" % self.hour)

    def clean(self):
        # If not surveying, ensure grid_tile and kea are unset.
        if self.activity == "X":
            self.grid_tile = None
            self.kea = False
        else:
            # If any other status, must have a grid tile.
            if self.grid_tile is None:
                raise ValidationError('Hours surveyed must have a grid tile.')
        super().clean()

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
