from django.db import models
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.core.validators import RegexValidator

from locations.models import AreaLocation
from keadatabase.choices import *


# Models
class BandCombo(models.Model):
    """ BandCombo, made up of multiple Band models. """
    # Fields
    ## Basic details
    combo_type = models.CharField(max_length=1, choices=COMBO_TYPE_CHOICES, default='N')
    area_location = models.ForeignKey(AreaLocation, blank=True, null=True)

    ## Validation helper for primary (TODO: fix)
    primary_count = 0

    ## Helper field for display
    display = models.CharField(max_length=255, editable=False)


    # Validation
    def clean(self):
        """ Validate various model fields to ensure uniqueness and consistency """
        errors = {}

        ## Validation of combo_type and primary bands occurs in Band model.

        if errors:
            raise ValidationError(errors)


    # Functions
    def get_display(self):
        """ Create human readable string depending on bands and combo_type """
        ## TODO: confirm if order is important (e.g. L leg then R leg)??
        output = []
        if self.band_set.all():
            bands_str = []
            for band in self.band_set.all():
                if str(band) not in bands_str:
                    bands_str.append(str(band))
            output.append(' | '.join(bands_str))
        if not output:
            return 'Unknown'
        return ' '.join(output)


    def __str__(self):
        return self.display


    # Transformation
    def save(self, *args, **kwargs):
        """ Update non-editable field containing display """
        self.display = self.get_display()
        super(BandCombo, self).save(*args, **kwargs)


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
    colour = models.CharField(max_length=10, blank=True, choices=BAND_COLOUR_CHOICES, default='')
    position = models.CharField(max_length=1, blank=True, choices=BAND_POSITION_CHOICES, default='')
    leg = models.CharField(max_length=1, blank=True, choices=BAND_LEG_CHOICES, default='')

    ## Letter (New)
    symbol_colour = models.CharField(max_length=10, blank=True, choices=BAND_SYMBOL_COLOUR_CHOICES,
                                     default='')
    symbol = models.CharField(max_length=10, blank=True, choices=BAND_SYMBOL_CHOICES, default='')

    ## Helper field for band_type
    band_type = models.CharField(max_length=1, editable=False, choices=BAND_TYPE_CHOICES)


    # Meta
    class Meta:
        unique_together = ('style', 'identifier', 'colour', 'leg', 'position', 'symbol_colour',
                           'symbol', 'size',)


    # Validation
    def clean(self):
        """ Validate various model fields to ensure uniqueness and consistency """
        errors = {}
        band_type = self.get_band_type()

        ## Model needs to validate that the band is a complete band for one of the three types
        if band_type == '?':
            errors.update({NON_FIELD_ERRORS: 'Band type unable to be identified. ' \
                                             'Please provide more information.'})

        ## Validations if assigned to BandCombo
        if self.band_combo:
            ### Band needs to be the correct type for the BandCombo (N/O)
            if self.band_combo.combo_type != band_type and band_type != 'M':
                errors.update({NON_FIELD_ERRORS: 'Invalid band type for BandCombo. ' \
                                                 'Please change the Band or BandCombo type.'})

            ### If primary, Band needs to be the only primary field
            if self.primary:
                self.band_combo.primary_count += 1

            if self.band_combo.primary_count > 1:
                errors.update({NON_FIELD_ERRORS: 'Cannot have more than one primary band. ' \
                                                 'Please select a single band as primary.'})

        if errors:
            raise ValidationError(errors)


    # Functions
    def get_bird_display(self):
        """ Display bird str if allocated to a BandCombo (in turn, allocated to a Bird) """
        if self.band_combo:
            if hasattr(self.band_combo, 'bird'):
                return str(self.band_combo.bird)
        return '-'
    get_bird_display.short_description = 'Bird'


    def get_band_type(self):
        """ Determines the BAND_TYPE_CHOICES of the band, based on fields completed """
        if self.colour and self.symbol_colour and self.symbol and self.style == 'P':
            return 'N' # Letter (New)
        elif self.colour and self.colour != 'UNCOLOURED' and self.position and self.leg \
             and not self.symbol and not self.symbol_colour:
            return 'O' # Colour (Old)
        elif self.colour == 'UNCOLOURED' and self.style == 'M' and self.identifier:
            return 'M' # Identifier (Metal)
        return '?'


    def get_combo_display(self):
        """ Create human readable combo based on the band_type """
        if self.band_type == 'N':
            return '%s "%s" on %s' % (self.get_symbol_colour_display(), self.symbol,
                                      self.get_colour_display())
        elif self.band_type == 'O':
            return '%s %s %s' % (self.get_colour_display(), self.get_position_display(),
                                 self.get_leg_display())
        return ''


    def __str__(self):
        """ Creates human readable string based on type of Band """
        output = []
        if self.get_combo_display():
            output.append(self.get_combo_display())
        if self.identifier:
            output.append('[%s]' % (self.identifier))
        if self.size:
            output.append('(%s)' % (self.get_size_display()))
        if not output:
            return 'Unknown'
        else:
            return ' '.join(output)


    # Transformation
    def save(self, *args, **kwargs):
        """ Update non-editable field containing band_type """
        self.band_type = self.get_band_type()
        super(Band, self).save(*args, **kwargs)
