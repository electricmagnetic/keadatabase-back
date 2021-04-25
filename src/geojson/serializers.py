from rest_framework_gis.serializers import GeoFeatureModelSerializer

from sightings.serializers.observations import ObservationSerializer
from sightings.serializers.birds import BirdObservationSerializer

from locations.models import GridTile
from locations.serializers import GridTileSerializer


class ObservationGeoJSONSerializer(
    GeoFeatureModelSerializer, ObservationSerializer
):
    class Meta(ObservationSerializer.Meta):
        geo_field = 'point_location'


class GridTileGeoJSONSerializer(GeoFeatureModelSerializer, GridTileSerializer):
    class Meta:
        model = GridTile
        geo_field = 'polygon'
        fields = '__all__'


class BirdObservationGeoJSONSerializer(
    GeoFeatureModelSerializer, BirdObservationSerializer
):
    class Meta(BirdObservationSerializer.Meta):
        geo_field = 'sighting__point_location'
