""" Contributor model for sightings (sightings and non-sightings in .sightings)"""

from django.db import models

ACTIVITY_CHOICES = (
    ('', ''),
    ('tourist', 'Tourist'),
    ('local', 'Local'),
    ('school', 'School Group'),
    ('community', 'Community Group'),
    ('skier', 'Skier'),
    ('tramper', 'Tramper'),
    ('hunter', 'Hunter'),
    ('birder', 'Birder'),
    ('doc', 'DOC Staff'),
    ('research', 'Researcher'),
    ('other', 'Other'),
)

HEARD_CHOICES = (
    ('', ''),
    ('shelter', 'Kea Information Shelter'),
    ('poster', 'Poster'),
    ('brochure', 'Brochure'),
    ('social', 'Social Media'),
    ('news', 'News'),
    ('friend', 'From a friend'),
    ('other', 'Other'),
)

class SightingsContributor(models.Model):
    """ Contributor details for a particular sighting """
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)

    # Optional
    phone = models.CharField(max_length=50, blank=True, null=True)

    activity = models.CharField(max_length=15, blank=True, choices=ACTIVITY_CHOICES, default='')
    heard = models.CharField(max_length=15, blank=True, choices=HEARD_CHOICES, default='')

    communications = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'contributor'

    def __str__(self):
        return self.name
