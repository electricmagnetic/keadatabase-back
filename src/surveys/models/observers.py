from django.db import models

from .choices import PURPOSE_CHOICES

class Observer(models.Model):
    """ Observer details for a particular survey """
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)

    # Optional
    purpose = models.CharField(max_length=15, blank=True, choices=PURPOSE_CHOICES, default='')

    def __str__(self):
        return self.name
