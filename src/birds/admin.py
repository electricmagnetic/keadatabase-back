from django.contrib import admin

from .models import Bird, BirdExtended

class BirdAdmin(admin.ModelAdmin):
    search_fields = ('name',)

class BirdExtendedAdmin(admin.ModelAdmin):
    list_filter = ('is_featured',)
    search_fields = ('bird__name',)

admin.site.register(Bird, BirdAdmin)
admin.site.register(BirdExtended, BirdExtendedAdmin)
