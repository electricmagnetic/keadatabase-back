from django.contrib.gis import admin

from .models.contributors import SightingsContributor
#from .models.media import SightingsMedia
from .models.sightings import SightingsNonSighting, SightingsSighting
from .models.birds import SightingsBird

class SightingsBirdInline(admin.TabularInline):
    model = SightingsBird
    extra = 0

class SightingsSightingAdmin(admin.OSMGeoAdmin):
    list_display = ('__str__', 'contributor', 'region', 'quality', 'date_created',)
    inlines = [SightingsBirdInline]

class SightingsNonSightingAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'contributor', 'region', 'quality', 'date_created',)

admin.site.register(SightingsContributor)
#admin.site.register(SightingsMedia)

admin.site.register(SightingsNonSighting, SightingsNonSightingAdmin)
admin.site.register(SightingsSighting, SightingsSightingAdmin)
admin.site.register(SightingsBird)
