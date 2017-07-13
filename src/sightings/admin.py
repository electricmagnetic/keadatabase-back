from django.contrib import admin

from .models.contributors import SightingsContributor
from .models.media import SightingsMedia
from .models.sightings import SightingsNonSighting, SightingsSighting
from .models.birds import SightingsBird

admin.site.register(SightingsContributor)
admin.site.register(SightingsMedia)

admin.site.register(SightingsNonSighting)
admin.site.register(SightingsSighting)
admin.site.register(SightingsBird)
