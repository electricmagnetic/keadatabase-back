from django.conf import settings
from django.contrib.gis.db.models.functions import Distance


def get_place_string(instance):
    """ Return closest Place (as string) to point_location coordinates """
    from locations.models import Place

    return str(
        Place.objects.annotate(
            distance=Distance('point', instance.point_location)
        ).order_by('distance').first()
    )


def get_region_string(instance):
    """ Return the Region (as string) that point_location is contained within """
    from locations.models import Region

    return str(Region.objects.get(polygon__contains=instance.point_location))


def run_geocode(sender, instance, **kwargs):
    """ Provide location based information """
    # Geocode place
    try:
        place_string = get_place_string(instance)
    except:
        pass
    else:
        instance.geocode = place_string

    # Geocode region
    try:
        region_string = get_region_string(instance)
    except:
        pass
    else:
        instance.region = region_string
