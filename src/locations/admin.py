from django.contrib.gis import admin

from .models import StudyArea, Region, Place

admin.site.register(StudyArea)
admin.site.register(Region)
admin.site.register(Place, admin.OSMGeoAdmin)
