from django.contrib.gis import admin

from .models.contributors import Contributor
from .models.media import SightingsMedia
from .models.sightings import NonSighting, Sighting
from .models.birds import BirdSighting

class SightingImportReport(Sighting):
    """ Proxy model for showing different view of sightings """

    class Meta:
        proxy = True
        verbose_name = 'Import report'

class SightingImportReportAdmin(admin.ModelAdmin):
    """ Read only view of sightings with import_id """

    list_display = ('id', '__str__', 'import_id',)
    search_fields = ('import_id',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

class ContributorAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'email', 'activity', 'heard', 'communications',)

class BirdSightingInline(admin.TabularInline):
    model = BirdSighting
    extra = 0

class SightingsMediaInline(admin.StackedInline):
    model = SightingsMedia
    extra = 0

class SightingAdmin(admin.OSMGeoAdmin):
    list_display = ('id', '__str__', 'contributor', 'region', 'geocode', 'quality', 'date_created', 'favourite',)
    list_filter = ('quality', 'date_created', 'favourite', 'region',)
    inlines = [BirdSightingInline, SightingsMediaInline]
    readonly_fields = ('geocode', 'region', 'import_id',)
    search_fields = ('id__exact',)

class NonSightingAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'contributor', 'region', 'quality', 'date_created',)

class BirdSightingAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'banded', 'sex_guess', 'life_stage_guess', 'band_combo', 'bird',
                    'revisit',)
    list_filter = ('revisit',)

admin.site.register(Contributor, ContributorAdmin)
admin.site.register(SightingsMedia)

admin.site.register(NonSighting, NonSightingAdmin)
admin.site.register(Sighting, SightingAdmin)
admin.site.register(BirdSighting, BirdSightingAdmin)

admin.site.register(SightingImportReport, SightingImportReportAdmin)
