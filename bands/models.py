from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from locations.models import PrimaryLocation
from keadatabase.choices import *


# Models
class Band(models.Model):
    """ Band, allows for multiple types. Can be associated with a bird via a BandCombo. """
    # Fields
    ## Common
    style = models.CharField(max_length=2, blank=True, choices=BAND_STYLE_CHOICES, default='')
    identifier = models.CharField(max_length=200, null=True, blank=True,
                                  validators=[
                                      RegexValidator(regex='^[a-z0-9]{1,2}-[0-9]+$',
                                                     message='ID band must be a lowercase series ' \
                                                     'of letters or numbers followed by a dash ' \
                                                     'then a series of numbers. No spaces.')
                                  ])
    colour = models.CharField(max_length=8, choices=BAND_COLOUR_CHOICES, default='BLACK')


    ## Old style
    leg = models.CharField(max_length=1, blank=True, choices=BAND_LEG_CHOICES, default='')
    position = models.CharField(max_length=1, blank=True, choices=BAND_POSITION_CHOICES, default='')


    ## New style
    symbol = models.CharField(max_length=10, blank=True, choices=BAND_SYMBOL_CHOICES, default='')
    symbol_colour = models.CharField(max_length=8, choices=BAND_SYMBOL_COLOUR_CHOICES,
                                     default='WHITE')
    size = models.CharField(max_length=2, blank=True, choices=BAND_SIZE_CHOICE, default='')


    # Meta
    class Meta:
        unique_together = ('style', 'identifier', 'colour', 'leg', 'position', 'symbol',
                           'symbol_colour', 'size',)


# class BandCombo(models.Model):
#     """ BandCombo, made up of multiple Band models. """
#     # Fields
#     ## Location
#     primary_location = models.ForeignKey(PrimaryLocation, blank=True, null=True)
#
#
#     # Functions
#     def get_colour_band(self):
#         """ Creates string containing colour band information """
#         if self.band_colour or self.band_symbol_colour or self.band_symbol:
#             return '%s "%s" on %s' % (self.get_band_symbol_colour_display(),
#                                       self.band_symbol,
#                                       self.get_band_colour_display())
#         else:
#             return '-'
#     get_colour_band.short_description = 'Colour band'
#
#
#     def get_colour_band_code(self):
#         """ Creates unique code for colour band combination """
#         if self.band_colour or self.band_symbol_colour or self.band_symbol:
#             return '%s-%s_%s' % (self.band_symbol_colour, self.band_symbol,
#                                  self.band_colour)
#         else:
#             return ''
#     get_colour_band_code.short_description = 'Colour band code'
#
#
#     def get_bird(self):
#         """ Get bird associated with this band """
#         return str(self.bird)
#     get_bird.short_description = 'Bird'
#
#
#     def __str__(self):
#         return self.get_colour_band()
#
#
#     # Transformation
#     def save(self, *args, **kwargs):
#         """ Transform various model fields for consistency """
#         ## Transform characters to uppercase in band_symbol
#         self.band_symbol = self.band_symbol.upper()
#
#         super(Band, self).save(*args, **kwargs)
#
#
#     # Validation
#     def clean(self):
#         """ Validate various model fields to ensure uniqueness and consistency """
#         errors = {}
#
#         ## Validate that only fully completed colour bands are entered (i.e. no partial bands)
#         if self.band_colour or self.band_symbol_colour or self.band_symbol:
#             if not self.band_colour:
#                 errors.update({'band_colour': 'Cannot leave colour band partially ' \
#                                               'complete. Please fill out remainder.'})
#             if not self.band_symbol_colour:
#                 errors.update({'band_symbol_colour': 'Cannot leave colour band partially ' \
#                                                      'complete. Please fill out remainder.'})
#             if not self.band_symbol:
#                 errors.update({'band_symbol': 'Cannot leave colour band partially ' \
#                                               'complete. Please fill out remainder.'})
#
#         ## If any errors occur, raise them
#         if errors:
#             raise ValidationError(errors)
