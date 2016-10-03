from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from locations.models import PrimaryLocation


# Choices
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
class Band(models.Model):
    """ Available band combinations """
    # Fields
    ## Location
    primary_location = models.ForeignKey(PrimaryLocation, blank=True, null=True)


    ## ID band
    id_band = models.CharField(max_length=200, verbose_name='ID band (v-band)', unique=True,
                               validators=[
                                   RegexValidator(regex='^[a-z0-9]{1,2}-[0-9]+$',
                                                  message='ID band must be a lowercase series of ' \
                                                  'letters or numbers followed by a dash then a ' \
                                                  'series of numbers. No spaces.')
                               ])


    ## Colour band
    colour_band_type = models.CharField(max_length=1, blank=True, choices=BAND_TYPE_CHOICES,
                                        verbose_name='Colour band type', default='')
    colour_band_symbol_colour = models.CharField(max_length=8, blank=True,
                                                 choices=BAND_SYMBOL_COLOUR_CHOICES, default='')
    colour_band_symbol = models.CharField(max_length=1, blank=True)
    colour_band_colour = models.CharField(max_length=8, blank=True, choices=BAND_COLOUR_CHOICES,
                                          default='')


    # Functions
    def get_colour_band(self):
        """ Creates string containing colour band information """
        if self.colour_band_colour or self.colour_band_symbol_colour or self.colour_band_symbol:
            return '%s "%s" on %s' % (self.get_colour_band_symbol_colour_display(),
                                      self.colour_band_symbol,
                                      self.get_colour_band_colour_display())
        else:
            return '-'
    get_colour_band.short_description = 'Colour band'


    def get_colour_band_code(self):
        """ Creates unique code for colour band combination """
        if self.colour_band_colour or self.colour_band_symbol_colour or self.colour_band_symbol:
            return '%s-%s_%s' % (self.colour_band_symbol_colour, self.colour_band_symbol,
                                 self.colour_band_colour)
        else:
            return ''
    get_colour_band_code.short_description = 'Colour band code'


    def get_bird(self):
        """ Get bird associated with this band """
        return str(self.bird)
    get_bird.short_description = 'Bird'


    def __str__(self):
        return self.id_band


    # Transformation
    def save(self, *args, **kwargs):
        """ Transform various model fields for consistency """
        ## Transform characters to uppercase in colour_band_symbol
        self.colour_band_symbol = self.colour_band_symbol.upper()

        super(Band, self).save(*args, **kwargs)


    # Validation
    def clean(self):
        """ Validate various model fields to ensure uniqueness and consistency """
        errors = {}

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

    # TODO validate colour band is unique in one primary location (unique together?)
    # TODO enable search by colour band (index together?)
