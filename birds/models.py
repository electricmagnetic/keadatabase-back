from django.db import models

from locations.models import PrimaryLocation, SecondaryLocation


class Bird(models.Model):
    """ Information on existing banded birds """

    # Choices
    SEX_CHOICES = (
        ('', 'Unknown'),
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
        ('A', 'Alive'),
        ('D', 'Dead'),
    )

    LEG_CHOICES = (
        ('', 'Unknown'),
        ('L', 'Left'),
        ('R', 'Right'),
    )

    COLOUR_CHOICES = (
        ('', 'Unknown'),
        ('BLACK', 'Black'),
        ('WHITE', 'White'),
        ('RED', 'Red'),
        ('ORANGE', 'Orange'),
        ('YELLOW', 'Yellow'),
        ('GREEN', 'Green'),
        ('BLUE', 'Blue'),
        ('PURPLE', 'Purple'),
        ('GREY', 'Grey'),
    )

    BAND_CHOICES = (
        ('', 'Unknown'),
        ('P', 'Plastic (modern)'),
        ('M', 'Metal (historic)'),
    )


    # Fields
    ## Basic details
    name = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=1, blank=True, choices=STATUS_CHOICES, default='A')
    sex = models.CharField(max_length=1, blank=True, choices=SEX_CHOICES, default='')
    life_stage = models.CharField(max_length=1, blank=True, choices=LIFE_STAGE_CHOICES, default='')
    age = models.IntegerField(blank=True, null=True, verbose_name='Approximate age (years)')
    family = models.CharField(max_length=200, blank=True)


    ## Location details
    primary_location = models.ForeignKey(PrimaryLocation, blank=True, null=True)
    secondary_location = models.ForeignKey(SecondaryLocation, blank=True, null=True)


    ## Catch details
    date_caught = models.DateField(blank=True, null=True)

    caught_by = models.CharField(max_length=200, blank=True)
    banded_by = models.CharField(max_length=200, blank=True)

    caught_longitude = models.DecimalField(max_digits=12, decimal_places=8, blank=True, null=True)
    caught_latitude = models.DecimalField(max_digits=12, decimal_places=8, blank=True, null=True)


    ## Band details
    id_band_type = models.CharField(max_length=1, blank=True, choices=BAND_CHOICES,
                                    verbose_name='ID band type', default='')
    id_band_leg = models.CharField(max_length=1, blank=True, choices=LEG_CHOICES,
                                   verbose_name='ID band leg (primary)', default='')
    id_band = models.CharField(max_length=200, verbose_name='ID band (V-band)')

    colour_band_colour = models.CharField(max_length=8, blank=True, choices=COLOUR_CHOICES,
                                          default='')
    colour_band_symbol = models.CharField(max_length=1, blank=True)
    colour_band_symbol_colour = models.CharField(max_length=8, blank=True, choices=COLOUR_CHOICES,
                                                 default='')


    ## Transmitter details
    transmitter = models.BooleanField()
    transmitter_channel = models.CharField(max_length=10, blank=True)


    ## Notes
    health = models.TextField(blank=True)
    notes = models.TextField(blank=True)


    ## Metadata
    date_updated = models.DateTimeField(auto_now=True)


    # Functions
    def get_identifier(self):
        """ Creates string for identifying bird """

        if self.name:
            return self.name
        else:
            return self.id_band
    get_identifier.short_description = 'Identifier'


    def get_location(self):
        """ Creates string for location """

        if self.primary_location and self.secondary_location:
            return '%s (%s)' % (self.primary_location, self.secondary_location)
        else:
            return '%s' % (self.primary_location or self.secondary_location or '')
    get_location.short_description = 'Location'


    def get_id_band(self):
        """ Creates string containing ID band information """

        if self.id_band_leg:
            return '%s [%s]' % (self.id_band, self.id_band_leg)
        else:
            return self.id_band
    get_id_band.short_description = 'ID band'


    def get_colour_band(self):
        """ Creates string containing colour band information """

        if self.colour_band_colour or self.colour_band_symbol_colour or self.colour_band_symbol:
            return '%s band; %s "%s"' % (self.get_colour_band_colour_display(),
                                         self.get_colour_band_symbol_colour_display(),
                                         self.colour_band_symbol)
        else:
            return ''
    get_colour_band.short_description = 'Colour band'


    def __str__(self):
        return self.get_identifier()
