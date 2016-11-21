from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from locations.models import HomeLocation
from keadatabase.choices import *


# Models
class BandCombo(models.Model):
    """ BandCombo, made up of multiple Band models. """
    # Fields
    ## Basic details
    status = models.CharField(max_length=1, choices=BAND_STATUS_CHOICES, default='+')
    combo_type = models.CharField(max_length=1, choices=COMBO_TYPE_CHOICES, default='L')
    home_location = models.ForeignKey(HomeLocation, blank=True, null=True)


class Band(models.Model):
    """ Band, allows for multiple types. Can be associated with a bird via a BandCombo. """
    # Fields
    ## Foreign key
    band_combo = models.ForeignKey(BandCombo, blank=True, null=True, on_delete=models.CASCADE)


    ## Common
    primary = models.BooleanField(default=False)
    style = models.CharField(max_length=2, blank=True, choices=BAND_STYLE_CHOICES, default='')
    identifier = models.CharField(max_length=200, null=True, blank=True,
                                  validators=[
                                      RegexValidator(regex='^[a-z0-9]{1,2}-[0-9]+$',
                                                     message='ID band must be a lowercase series ' \
                                                     'of letters or numbers followed by a dash ' \
                                                     'then a series of numbers. No spaces.')
                                  ])
    size = models.CharField(max_length=2, blank=True, choices=BAND_SIZE_CHOICE, default='')
    colour = models.CharField(max_length=8, blank=True, choices=BAND_COLOUR_CHOICES, default='')
    position = models.CharField(max_length=1, blank=True, choices=BAND_POSITION_CHOICES, default='')
    leg = models.CharField(max_length=1, blank=True, choices=BAND_LEG_CHOICES, default='')


    ## Letter (New)
    symbol_colour = models.CharField(max_length=8, blank=True, choices=BAND_SYMBOL_COLOUR_CHOICES,
                                     default='')
    symbol = models.CharField(max_length=10, blank=True, choices=BAND_SYMBOL_CHOICES, default='')


    # Meta
    class Meta:
        unique_together = ('style', 'identifier', 'colour', 'leg', 'position', 'symbol_colour',
                           'symbol', 'size',)


    # Validation
    def clean(self):
        """ Validate various model fields to ensure uniqueness and consistency """
        errors = {}

        ## Model needs to validate that the band is a complete band for one of three types:
        ## (a) Letter (New) (b) colour (c) metal


        # if self.band_colour or self.band_symbol_colour or self.band_symbol:
        #     if not self.band_colour:
        #         errors.update({'band_colour': 'Cannot leave colour band partially ' \
        #                                       'complete. Please fill out remainder.'})
        #     if not self.band_symbol_colour:
        #         errors.update({'band_symbol_colour': 'Cannot leave colour band partially ' \
        #                                              'complete. Please fill out remainder.'})
        #     if not self.band_symbol:
        #         errors.update({'band_symbol': 'Cannot leave colour band partially ' \
        #                                       'complete. Please fill out remainder.'})

        ## If any errors occur, raise them
        if errors:
            raise ValidationError(errors)


    # Functions
    def get_bird(self):
        """ Display bird if allocated to a BandCombo (in turn, allocated to a Bird) """
        if self.band_combo:
            if self.band_combo.bird:
                return str(self.band_combo.bird)
        return 'Unallocated'
    get_bird.short_description = 'Bird'


    def get_band_type(self):
        """ Determines the BAND_TYPE_CHOICES of the band, based on fields completed """
        if self.style == 'P' and self.colour and self.symbol_colour and self.symbol:
            return 'N' # Letter (New)
        elif self.style == 'UM' and self.identifier:
            return 'M' # Identifier (Metal)
        elif self.colour and self.position and self.leg:
            return 'O' # Colour (Old)
        return 'Unknown'


    def get_band_type_display(self):
        """ Human readable representation of get_band_type """
        band_type = self.get_band_type()

        if band_type and band_type != 'Unknown':
            return dict(BAND_TYPE_CHOICES)[band_type]
        else:
            return band_type
    get_band_type_display.short_description = 'Type'


    def get_band_combo_display(self):
        """ Creates human readable string based on allocation to BandCombo """
        if self.band_combo:
            return str(self.band_combo)
        else:
            return 'Unallocated'
    get_band_combo_display.short_description = 'Combo'


    def __str__(self):
        """ Creates human readable string based on type of band """
        output = []

        if self.get_band_type() == 'N':
            output.append('%s "%s" on %s' % (self.get_symbol_colour_display(), self.symbol,
                                             self.get_colour_display()))
        elif self.get_band_type() == 'O':
            output.append('%s %s %s' % (self.get_colour_display(), self.get_position_display(),
                                        self.get_leg_display()))

        if self.identifier:
            output.append('[%s]' % (self.identifier))

        if self.size:
            output.append('(%s)' % (self.get_size_display()))

        if not output:
            return 'Unknown'
        else:
            return ' '.join(output)
