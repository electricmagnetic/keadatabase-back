from django.contrib import admin

from .models import Bird, BirdExtended

class BirdAdmin(admin.ModelAdmin):
    search_fields = ('name', 'primary_band',)
    list_display = ('__str__', 'primary_band', 'band_combo', 'study_area',)
    list_per_page = 250

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.all().select_related("bird_extended", "study_area", "band_combo")

class BirdExtendedAdmin(admin.ModelAdmin):
    list_filter = ('is_featured',)
    search_fields = ('bird__name',)

admin.site.register(Bird, BirdAdmin)
admin.site.register(BirdExtended, BirdExtendedAdmin)
