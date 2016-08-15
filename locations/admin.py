from django.contrib import admin

from .models import PrimaryLocation, SecondaryLocation


admin.site.register(PrimaryLocation)
admin.site.register(SecondaryLocation)
