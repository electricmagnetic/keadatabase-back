from django.contrib import admin

from .models.observers import Observer
from .models.surveys import Survey, SurveyHour

class ObserverAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'email', 'purpose',)

class SurveyHourInline(admin.StackedInline):
    model = SurveyHour
    extra = 0
    list_select_related = True
    raw_id_fields = ('grid_tile',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.all(). \
            select_related('survey', 'grid_tile'). \
            all()

class SurveyAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'date', 'max_flock_size', 'observer', 'status',)
    list_filter = ('date', 'status',)
    inlines = [SurveyHourInline]
    search_fields = ('id__exact',)
    list_select_related = True

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.all().select_related('observer').prefetch_related('hours')

class SurveyHourAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'survey', 'hour', 'kea', 'activity', 'grid_tile',)
    list_filter = ('kea', 'activity',)
    list_select_related = True
    raw_id_fields = ('grid_tile',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.all().select_related('survey', 'grid_tile',)

admin.site.register(Observer, ObserverAdmin)
admin.site.register(Survey, SurveyAdmin)
admin.site.register(SurveyHour, SurveyHourAdmin)
