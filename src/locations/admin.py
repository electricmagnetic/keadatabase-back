from django.contrib.gis import admin

from .models import StudyArea, Region, CommonLocation

admin.site.register(StudyArea)
admin.site.register(Region)
admin.site.register(CommonLocation, admin.OSMGeoAdmin)
