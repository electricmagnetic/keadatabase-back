from rest_framework_gis.serializers import GeoFeatureModelSerializer

from sightings.models.sightings import Sighting
from sightings.serializers.sightings import SightingSerializer
from sightings.serializers.birds import BirdSightingSerializer

from locations.models import GridTile
from locations.serializers import GridTileSerializer

class SightingGeoJSONSerializer(GeoFeatureModelSerializer, SightingSerializer):
    class Meta(SightingSerializer.Meta):
        geo_field = 'point_location'

class GridTileGeoJSONSerializer(GeoFeatureModelSerializer, GridTileSerializer):
    class Meta:
        model = GridTile
        geo_field = 'polygon'
        fields = '__all__'

class BirdSightingGeoJSONSerializer(GeoFeatureModelSerializer, BirdSightingSerializer):
    class Meta(BirdSightingSerializer.Meta):
        geo_field = 'sighting__point_location'
