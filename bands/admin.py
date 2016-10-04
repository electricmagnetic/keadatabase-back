from django.contrib import admin

from .models import Band
from .forms import BandForm

class BandAdmin(admin.ModelAdmin):
    """ Defines the fieldsets for the Band model admin """
    form = BandForm

    fieldsets = [
        ('Location', {'fields':[
            ('primary_location',)
        ]}),
        ('Band', {'fields':[
            'band_type',
            ('band_symbol_colour', 'band_symbol', 'band_colour')
        ]}),
    ]

    list_display = ('get_colour_band', 'primary_location', 'get_bird',)


admin.site.register(Band, BandAdmin)
