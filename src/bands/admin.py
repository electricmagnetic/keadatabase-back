from django.contrib import admin

from .models import BandCombo


class BandComboAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'bird',
        'study_area',
        'date_modified',
    )
    search_fields = (
        'name__icontains',
        'bird__name',
    )
    list_per_page = 250


admin.site.register(BandCombo, BandComboAdmin)
