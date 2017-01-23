from django.contrib.gis import admin

from .models import Bird, BirdSighting
from .forms import BirdForm


class BirdAdmin(admin.GeoModelAdmin):
    """ Defines the fieldsets for the Bird model admin """
    form = BirdForm

    list_display = ('get_identifier', 'status',  'home_location', 'life_stage', 'date_updated',)
    list_filter = ('status', 'sex', 'life_stage',)
    search_fields = ['name']

    fieldsets = [
        (None, {'fields':[
            'name', 'status', 'sex', 'life_stage', 'birthday', 'description', 'photo', 'band_combo',
        ]}),
        ('Location', {'fields':[
            ('home_location')
        ]}),
        ('Notes', {'fields':[
            'health', 'notes'
        ]}),
    ]


admin.site.register(Bird, BirdAdmin)


class BirdSightingAdmin(admin.GeoModelAdmin):
    """ Defines the fieldsets for the BirdSighting model admin """
    list_display = ('sighting', 'verification', 'bird',)
    list_filter = ('verification',)

    fieldsets = [
        (None, {'fields':[
            'sighting'
        ]}),
        ('Kea details', {'fields':[
            'status', 'sex', 'life_stage'
        ]}),
        # ('Band details', {'fields':[
        #     'banded', 'band_type', 'band_colour', 'band_symbol',
        #     'band_symbol_colour'
        # ]}),
        ('Verification', {'fields':[
            'verification'
        ]}),
        ('Kea match', {'fields':[
            'bird'
        ]}),
    ]


admin.site.register(BirdSighting, BirdSightingAdmin)
