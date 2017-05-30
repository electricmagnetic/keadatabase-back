from django.db import models
from django.utils.text import slugify

from locations.models import StudyArea

SEX_CHOICES = (
    ('', 'Undetermined'),
    ('F', 'Female'),
    ('M', 'Male'),
)

LIFE_STAGE_CHOICES = (
    ('', 'Unknown'),
    ('A', 'Adult'),
    ('S', 'Sub-adult'),
    ('J', 'Juvenile'),
    ('F', 'Fledgling'),
)

STATUS_CHOICES = (
    ('', 'Unknown'),
    ('+', 'Alive'),
    ('-', 'Dead'),
)

class Bird(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.CharField(max_length=100, primary_key=True, editable=False)

    sex = models.CharField(max_length=1, blank=True, choices=SEX_CHOICES,
                           default='')
    status = models.CharField(max_length=1, blank=True, choices=STATUS_CHOICES,
                              default='')
    birthday = models.DateField(blank=True, null=True)

    study_area = models.ForeignKey(StudyArea, blank=True, null=True)

    date_modified = models.DateTimeField(auto_now=True)
    date_imported = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """ Generate slug from name """
        self.slug = slugify(self.name)
        super(Bird, self).save(*args, **kwargs)
