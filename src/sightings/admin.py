from django.contrib.gis import admin

from .models.contributors import SightingsContributor
from .models.media import SightingsMedia
from .models.sightings import SightingsNonSighting, SightingsSighting
from .models.birds import SightingsBird

class SightingsContributorAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'email', 'activity', 'heard', 'communications',)

class SightingsBirdInline(admin.TabularInline):
    model = SightingsBird
    extra = 0

class SightingsMediaInline(admin.StackedInline):
    model = SightingsMedia
    extra = 0

class SightingsSightingAdmin(admin.OSMGeoAdmin):
    list_display = ('__str__', 'contributor', 'region', 'quality', 'date_created',)
    list_filter = ('quality', 'date_created',)
    inlines = [SightingsBirdInline, SightingsMediaInline]

class SightingsNonSightingAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'contributor', 'region', 'quality', 'date_created',)

class SightingsBirdAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'banded', 'sex_guess', 'life_stage_guess', 'band_combo', 'bird',
                    'revisit',)
    list_filter = ('revisit',)

admin.site.register(SightingsContributor, SightingsContributorAdmin)
admin.site.register(SightingsMedia)

admin.site.register(SightingsNonSighting, SightingsNonSightingAdmin)
admin.site.register(SightingsSighting, SightingsSightingAdmin)
admin.site.register(SightingsBird, SightingsBirdAdmin)
