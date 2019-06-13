from rest_framework_gis.serializers import GeoFeatureModelSerializer

from sightings.models.sightings import Sighting
from sightings.serializers.sightings import SightingSerializer

from locations.models import GridTile
from locations.serializers import GridTileSerializer

class SightingGeoJSONSerializer(GeoFeatureModelSerializer, SightingSerializer):
    class Meta(SightingSerializer.Meta):
        geo_field = 'point_location'

class GridTileGeoJSONSerializer(GeoFeatureModelSerializer, GridTileSerializer):
    class Meta(GridTileSerializer.Meta):
        geo_field = 'polygon'
