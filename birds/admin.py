from django.contrib import admin

from .models import Bird
from .forms import BirdForm


class BirdAdmin(admin.ModelAdmin):
    """ Defines the fieldsets for the Bird model admin """
    form = BirdForm

    list_display = ('get_identifier', 'status', 'life_stage', 'get_location', 'get_id_band',
                    'get_colour_band', 'date_updated',)

    list_filter = ('status', 'sex', 'life_stage',)

    fieldsets = [
        (None, {'fields':['name', 'status', 'sex', 'life_stage', 'age', 'family']}),
        ('Location', {'fields':['primary_location', 'secondary_location']}),
        ('Catch', {'fields':['date_caught', 'caught_by', 'banded_by', 'caught_longitude',
                             'caught_latitude']}),
        ('Band', {'fields':['id_band_type', 'id_band_leg', 'id_band', 'colour_band_colour',
                            'colour_band_symbol', 'colour_band_symbol_colour']}),
        ('Transmitter', {'fields':['transmitter', 'transmitter_channel']}),
        ('Notes', {'fields':['health', 'notes']}),
    ]


admin.site.register(Bird, BirdAdmin)
