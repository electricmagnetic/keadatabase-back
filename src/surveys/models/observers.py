from django.db import models

PURPOSE_CHOICES = (
    ('', ''),
    ('tunnel', 'Tracking Tunnel Check'),
    ('fwf', 'FWF Hunting'),
    ('hunt', 'Hunting'),
    ('guide', 'Guiding'),
    ('trap', 'Trapping'),
    ('permolat', 'Permolat/Hut/Track Work'),
    ('tramp', 'Tramping'),
    ('research', 'Researching'),
    ('kea', 'Kea Surveying'),
    ('hut', 'Hut Wardening'),
    ('other', 'Other'),
)

class Observer(models.Model):
    """ Observer details for a particular survey """
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)

    # Optional
    purpose = models.CharField(max_length=15, blank=True, choices=PURPOSE_CHOICES, default='')

    def __str__(self):
        return self.name
