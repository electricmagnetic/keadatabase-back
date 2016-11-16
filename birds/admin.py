from django.contrib.gis import admin
from django.conf import settings

from .models import Bird, BirdSighting
from .forms import BirdForm


class BirdAdmin(admin.GeoModelAdmin):
    """ Defines the fieldsets for the Bird model admin """
    form = BirdForm

    list_display = ('get_identifier', 'status',  'get_location', 'id_band', 'get_colour_band',
                    'life_stage', 'date_updated',)
    list_filter = ('status', 'sex', 'life_stage',)
    search_fields = ['name']

    fieldsets = [
        (None, {'fields':[
            'name', 'status', 'sex', 'life_stage', 'birthday', 'description', 'photo'
        ]}),
        ('Location', {'fields':[
            ('primary_location', 'secondary_location')
        ]}),
        ('Catch', {'fields':[
            'date_caught', ('caught_by', 'banded_by'), 'caught_location'
        ]}),
        ('Band', {'fields':[
            ('id_band_leg', 'id_band'), 'band'
        ]}),
        ('Transmitter', {'fields':[
            'transmitter_channel'
        ]}),
        ('Notes', {'fields':[
            'health', 'notes'
        ]}),
    ]

    default_lon = settings.GEO_DEFAULT_LON
    default_lat = settings.GEO_DEFAULT_LAT
    default_zoom = settings.GEO_DEFAULT_ZOOM

    wms_url = settings.GEO_WMS_URL
    wms_layer = settings.GEO_WMS_LAYER
    wms_name = settings.GEO_WMS_NAME
    wms_options = settings.GEO_WMS_OPTIONS


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
        ('Band details', {'fields':[
            'banded', 'band_type', 'band_colour', 'band_symbol',
            'band_symbol_colour'
        ]}),
        ('Verification', {'fields':[
            'verification'
        ]}),
        ('Kea match', {'fields':[
            'bird'
        ]}),
    ]


admin.site.register(BirdSighting, BirdSightingAdmin)
