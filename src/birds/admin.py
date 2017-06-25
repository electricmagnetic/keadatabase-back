from django.contrib import admin

from .models import Bird, BirdExtended

admin.site.register(Bird)
admin.site.register(BirdExtended)
