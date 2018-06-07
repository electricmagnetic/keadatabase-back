from django.conf import settings
from django.contrib.gis.db.models.functions import Distance

def run_geocode(sender, instance, **kwargs):
    coordinates = instance.point_location

    try:
        from locations.models import Place
        place_string = str(Place.objects.annotate(
            distance=Distance('point', instance.point_location)
        ).order_by('distance').first())
    except:
        pass
    else:
        instance.geocode = place_string
