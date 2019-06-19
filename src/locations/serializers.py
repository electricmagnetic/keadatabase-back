from rest_framework import serializers

from .models import GridTile
from surveys.serializers import SurveyHourSerializer

class GridTileSerializer(serializers.ModelSerializer):
    """ Default serializer """

    get_image = serializers.ReadOnlyField()
    hours = SurveyHourSerializer(many=True)

    class Meta:
        model = GridTile
        fields = '__all__'


class NoGeoGridTileSerializer(GridTileSerializer):
    """ Serializer excluding polygon field """

    class Meta:
        model = GridTile
        exclude = ('polygon',)
