from django.contrib.gis import admin
from django.conf import settings

from .models import PrimaryLocation, SecondaryLocation, HomeLocation


class PrimaryLocationAdmin(admin.GeoModelAdmin):
    """ Defines the table layout for primary locations """

    list_display = ('name',)
    search_fields = ['name']

    default_lon = settings.GEO_DEFAULT_LON
    default_lat = settings.GEO_DEFAULT_LAT
    default_zoom = settings.GEO_DEFAULT_ZOOM


class SecondaryLocationAdmin(admin.ModelAdmin):
    """ Defines the table layout for secondary locations """

    list_display = ('name', 'primary_location',)
    list_filter = ('primary_location',)
    search_fields = ['name']


admin.site.register(PrimaryLocation, PrimaryLocationAdmin)
admin.site.register(SecondaryLocation, SecondaryLocationAdmin)
admin.site.register(HomeLocation, PrimaryLocationAdmin)
