from django.contrib import admin

from .models import PrimaryLocation, SecondaryLocation


class PrimaryLocationAdmin(admin.ModelAdmin):
    """ Defines the table layout for primary locations """

    list_display = ('name',)


class SecondaryLocationAdmin(admin.ModelAdmin):
    """ Defines the table layout for secondary locations """

    list_display = ('name', 'primary_location',)

    list_filter = ('primary_location',)


admin.site.register(PrimaryLocation, PrimaryLocationAdmin)
admin.site.register(SecondaryLocation, SecondaryLocationAdmin)
