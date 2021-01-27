from rest_framework import serializers
from rest_framework_gis.serializers import GeometryField

from .models import GridTile


class BaseGridTileSerializer(serializers.Serializer):
    """ Default serializer """

    id = serializers.ReadOnlyField()

    get_large_image = serializers.ReadOnlyField()
    get_small_image = serializers.ReadOnlyField()

    min = GeometryField()
    max = GeometryField()

    centroid = GeometryField(precision=7)

    neighbours = serializers.ListField(child=serializers.CharField())

    hours_total = serializers.ReadOnlyField()
    hours_with_kea = serializers.ReadOnlyField()


class GridTileSerializer(BaseGridTileSerializer):
    """ Serializer including polygon field """

    polygon = GeometryField(precision=7)
