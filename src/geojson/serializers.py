from rest_framework_gis.serializers import GeoFeatureModelSerializer

from sightings.models.sightings import Sighting
from sightings.serializers.sightings import SightingSerializer

class SightingGeoJSONSerializer(GeoFeatureModelSerializer, SightingSerializer):
    class Meta(SightingSerializer.Meta):
        geo_field = 'point_location'
