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
            'id_band', 'colour_band_type',
            ('colour_band_symbol_colour', 'colour_band_symbol', 'colour_band_colour')
        ]}),
    ]

    list_display = ('id_band', 'get_colour_band', 'primary_location', 'get_bird',)


admin.site.register(Band, BandAdmin)
