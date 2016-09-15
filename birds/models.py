from datetime import date

from django.contrib.gis.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from locations.models import PrimaryLocation, SecondaryLocation
from sightings.models import Sighting


# Choices
BAND_CHOICES = (
    ('', 'Couldn\'t tell'),
    ('U', 'Banded, unreadable'),
    ('B', 'Banded, readable'),
    ('N', 'Not banded'),
)

VERIFICATION_CHOICES = (
    ('', 'Unverified'),
    ('Q', 'Questionable'),
    ('G', 'Good'),
    ('C', 'Confirmed'),
)

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

BAND_COLOUR_CHOICES = (
    ('', 'Unknown'),
    ('BLACK', 'Black'),
    ('WHITE', 'White'),
    ('RED', 'Red'),
    ('ORANGE', 'Orange'),
    ('YELLOW', 'Yellow'),
    ('GREEN', 'Green'),
    ('BLUE', 'Blue'),
    ('GREY', 'Grey'),
    ('O', 'Other'),
)

BAND_SYMBOL_COLOUR_CHOICES = (
    ('', 'Unknown'),
    ('BLACK', 'Black'),
    ('WHITE', 'White'),
    ('RED', 'Red'),
    ('YELLOW', 'Yellow'),
    ('O', 'Other'),
)

BAND_TYPE_CHOICES = (
    ('', 'Unknown'),
    ('P', 'Plastic (modern)'),
    ('M', 'Metal (historic)'),
)


# Models
class Bird(models.Model):
    """ Information on existing banded birds """
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

    caught_location = models.PointField(null=True, blank=True)


    ## Band details
    id_band_leg = models.CharField(max_length=1, blank=True, choices=LEG_CHOICES,
                                   verbose_name='ID band leg (primary)', default='')
    id_band = models.CharField(max_length=200, verbose_name='ID band (v-band)', unique=True,
                               validators=[
                                   RegexValidator(regex='^[a-z0-9]{1,2}-[0-9]+$',
                                                  message='ID band must be a lowercase series of ' \
                                                  'letters or numbers followed by a dash then a ' \
                                                  'series of numbers. No spaces.')
                               ])

    colour_band_type = models.CharField(max_length=1, blank=True, choices=BAND_TYPE_CHOICES,
                                        verbose_name='Colour band type', default='')
    colour_band_colour = models.CharField(max_length=8, blank=True, choices=BAND_COLOUR_CHOICES,
                                          default='')
    colour_band_symbol = models.CharField(max_length=1, blank=True)
    colour_band_symbol_colour = models.CharField(max_length=8, blank=True,
                                                 choices=BAND_SYMBOL_COLOUR_CHOICES, default='')


    ## Transmitter details
    transmitter_channel = models.CharField(max_length=10, blank=True)


    ## Notes
    health = models.TextField(blank=True)
    notes = models.TextField(blank=True)


    ## Media
    # TODO photo


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
        elif self.primary_location:
            return '%s' % (self.primary_location)
        else:
            return ''
    get_location.short_description = 'Location'


    def get_id_band(self):
        """ Creates string containing ID band information """

        if self.id_band_leg:
            return '%s [%s]' % (self.id_band, self.get_id_band_leg_display())
        else:
            return self.id_band
    get_id_band.short_description = 'ID band'


    def get_colour_band(self):
        """ Creates string containing colour band information """

        if self.colour_band_colour or self.colour_band_symbol_colour or self.colour_band_symbol:
            return '%s "%s" on %s' % (self.get_colour_band_symbol_colour_display(),
                                      self.colour_band_symbol,
                                      self.get_colour_band_colour_display())
        else:
            return ''
    get_colour_band.short_description = 'Colour band'


    def get_colour_band_code(self):
        """ Creates unique code for colour band combination """
        if self.colour_band_colour or self.colour_band_symbol_colour or self.colour_band_symbol:
            return '%s-%s_%s' % (self.colour_band_symbol_colour, self.colour_band_symbol,
                                 self.colour_band_colour)
        else:
            return ''


    def __str__(self):
        return self.get_identifier()


    # Transformation
    def save(self, *args, **kwargs):
        """ Transform various model fields for consistency """
        ## Transform characters to uppercase in colour_band_symbol
        self.colour_band_symbol = self.colour_band_symbol.upper()

        super(Bird, self).save(*args, **kwargs)


    # Validation
    def clean(self):
        """ Validate various model fields to ensure uniqueness and consistency """
        errors = {}

        ## Validate date_caught is not from the future
        current_date = date.today()
        if self.date_caught:
            if self.date_caught > current_date:
                errors.update({'date_caught': 'Date cannot be from the future.'})


        ## Validate secondary_location is paired with/is a child of primary_location
        if self.primary_location and self.secondary_location:
            if self.secondary_location.primary_location != self.primary_location:
                errors.update({'secondary_location': 'Secondary location must be in ' \
                                                              'primary location.'})
        elif self.secondary_location:
            errors.update({'primary_location': 'Must have primary location if secondary ' \
                                                        'location is specified.'})


        ## Validate that only fully completed colour bands are entered (i.e. no partial bands)
        if self.colour_band_colour or self.colour_band_symbol_colour or self.colour_band_symbol:
            if not self.colour_band_colour:
                errors.update({'colour_band_colour': 'Cannot leave colour band partially ' \
                                                     'complete. Please fill out remainder.'})
            if not self.colour_band_symbol_colour:
                errors.update({'colour_band_symbol_colour': 'Cannot leave colour band partially ' \
                                                            'complete. Please fill out remainder.'})
            if not self.colour_band_symbol:
                errors.update({'colour_band_symbol': 'Cannot leave colour band partially ' \
                                                     'complete. Please fill out remainder.'})


        ## If any errors occur, raise them
        if errors:
            raise ValidationError(errors)


    # TODO validate colour band is unique alive bird (in one primary location) (unique together?)
    # TODO enable search by colour band (index together?)


class BirdSighting(models.Model):
    """ Foreign key of Sighting, able to be verified and tagged to a particular Bird """
    # Fields
    ## Foreign key
    sighting = models.ForeignKey(Sighting, related_name='birds')


    ## Basic details
    status = models.CharField(max_length=1, blank=True, choices=STATUS_CHOICES, default='A')
    sex = models.CharField(max_length=1, blank=True, choices=SEX_CHOICES, default='')
    life_stage = models.CharField(max_length=1, blank=True, choices=LIFE_STAGE_CHOICES, default='')


    ## Band details
    banded = models.CharField(max_length=1, blank=True, choices=BAND_CHOICES, default='N')

    colour_band_type = models.CharField(max_length=1, blank=True, choices=BAND_TYPE_CHOICES,
                                        verbose_name='Colour band type', default='')
    colour_band_colour = models.CharField(max_length=8, blank=True, choices=BAND_COLOUR_CHOICES,
                                          default='')
    colour_band_symbol = models.CharField(max_length=1, blank=True)
    colour_band_symbol_colour = models.CharField(max_length=8, blank=True,
                                                 choices=BAND_SYMBOL_COLOUR_CHOICES, default='')


    ## Verification details (admin only)
    verification = models.CharField(max_length=1, blank=True, choices=VERIFICATION_CHOICES,
                                    default='')


    ## Bird details (admin only)
    bird = models.ForeignKey(Bird, blank=True, null=True, related_name='sightings')
