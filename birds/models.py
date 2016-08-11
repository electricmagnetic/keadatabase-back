from django.db import models


class Bird(models.Model):
    """ Information on existing banded birds """


    # Choices
    SEX_CHOICES = (
        ('u', 'Unknown'),
        ('F', 'Female'),
        ('M', 'Male'),
    )

    LIFE_STAGE_CHOICES = (
        ('u', 'Unknown'),
        ('A', 'Adult'),
        ('S', 'Sub-adult'),
        ('J', 'Juvenile'),
        ('F', 'Fledgling'),
    )


    # Fields
    ## Basic details
    name = models.CharField(max_length=200, blank=True)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default='u')
    life_stage = models.CharField(max_length=1, choices=LIFE_STAGE_CHOICES, default='u')
    #age = TBD
    family = models.CharField(max_length=200, blank=True)

    ## Catch details
    date_caught = models.DateField()
    caught_by = models.CharField(max_length=200)
    banded_by = models.CharField(max_length=200)
    # location_caught = TBD

    ## Band details
    # colour_band = TBD
    id_band = models.CharField(max_length=200, verbose_name='ID band (V-band)')
    transmitter = models.BooleanField()
    # transmitter_channel = TBD

    ## Notes
    notes = models.TextField()

    ## Metadata
    date_updated = models.DateTimeField(auto_now=True)


    # Functions
    def get_identifier(self):
        if self.name:
            return self.name
        else:
            return self.id_band

    def __str__(self):
        return self.get_identifier()

