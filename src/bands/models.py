from django.db import models

from birds.models import Bird

class BandCombo(models.Model):
    """ Basic band combo information, designed to be imported from Access """

    bird = models.OneToOneField(
        Bird,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['bird']

    def __str__(self):
        return self.name
