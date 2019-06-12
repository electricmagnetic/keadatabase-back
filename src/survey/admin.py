from django.contrib import admin

from .models.observers import Observer
from .models.surveys import Survey, SurveyHour

class ObserverAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'email',)

class SurveyHourInline(admin.StackedInline):
    model = SurveyHour
    extra = 0

class SurveyAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'date', 'max_flock_size', 'observer',)
    list_filter = ('date',)
    inlines = [SurveyHourInline]
    search_fields = ('id__exact',)


class SurveyHourAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'survey', 'hour', 'kea', 'status', 'grid_tile',)
    list_filter = ('kea', 'status',)


admin.site.register(Observer, ObserverAdmin)
admin.site.register(Survey, SurveyAdmin)
admin.site.register(SurveyHour, SurveyHourAdmin)
