from django.contrib.gis import admin

from .models import Bird, BirdExtended, BirdSighting

admin.site.register(Bird)
admin.site.register(BirdExtended)


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
