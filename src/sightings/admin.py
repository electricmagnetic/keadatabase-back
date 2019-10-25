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

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(import_id__isnull=False)

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
    raw_id_fields = ('bird',)

class SightingsMediaInline(admin.StackedInline):
    model = SightingsMedia
    extra = 0

def mark_public(modeladmin, request, queryset):
    queryset.update(status='public')
    mark_public.short_description = "Mark selected as Public"

def mark_fwf(modeladmin, request, queryset):
    queryset.update(status='fwf')
    mark_fwf.short_description = "Mark selected as FWF"

def mark_kct(modeladmin, request, queryset):
    queryset.update(status='kct')
    mark_kct.short_description = "Mark selected as KCT"

class SightingAdmin(admin.OSMGeoAdmin):
    list_display = ('id', '__str__', 'contributor', 'geocode', 'region', 'favourite', 'confirmed', 'status', 'date_created',)
    list_filter = ('status', 'date_created', 'favourite', 'region', 'confirmed',)
    inlines = [BirdSightingInline, SightingsMediaInline]
    readonly_fields = ('geocode', 'region', 'import_id',)
    search_fields = ('id__exact',)
    actions = [mark_public, mark_fwf, mark_kct]

class NonSightingAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'contributor', 'region', 'date_created', 'status',)

class BirdSightingAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'banded', 'sex_guess', 'life_stage_guess', 'band_combo', 'bird',
                    'revisit',)
    list_filter = ('revisit',)
    raw_id_fields = ('bird',)

admin.site.register(Contributor, ContributorAdmin)
admin.site.register(SightingsMedia)

admin.site.register(NonSighting, NonSightingAdmin)
admin.site.register(Sighting, SightingAdmin)
admin.site.register(BirdSighting, BirdSightingAdmin)

admin.site.register(SightingImportReport, SightingImportReportAdmin)
