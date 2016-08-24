from django.contrib.gis import admin
from django.conf import settings

from .models import Sighting
from birds.models import BirdSighting


class BirdSightingInline(admin.TabularInline):
    """ Inlines for each bird sighted """

    model = BirdSighting
    min_num = 1
    extra = 0
    max_num = 20
    can_delete = False


class SightingAdmin(admin.GeoModelAdmin):
    """ Defines the fieldsets for the Sighting model admin """

    list_display = ('date_sighted', 'time_sighted', 'primary_location', 'secondary_location',)

    fieldsets = [
        (None, {'fields':[('date_sighted', 'time_sighted')]}),
        ('Location details', {'fields':[('primary_location', 'secondary_location'),
                                        'point_location', 'point_accuracy', 'location_description'
                                       ]}),
        ('Notes', {'fields':['notes']}),
        ('Contributor details', {'fields':[('first_name', 'last_name'), ('email', 'newsletter'),
                                           'phone', 'category']}),
    ]

    inlines = (BirdSightingInline,)

    default_lon = settings.GEO_DEFAULT_LON
    default_lat = settings.GEO_DEFAULT_LAT
    default_zoom = settings.GEO_DEFAULT_ZOOM


admin.site.register(Sighting, SightingAdmin)
