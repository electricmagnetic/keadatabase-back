from rest_framework import serializers

from .models import GridTile
from surveys.serializers import SurveyHourSerializer

class GridTileSerializer(serializers.ModelSerializer):
    """ Default serializer """

    get_large_image = serializers.ReadOnlyField()
    get_small_image = serializers.ReadOnlyField()
    hours = SurveyHourSerializer(many=True)

    class Meta:
        model = GridTile
        fields = '__all__'

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.prefetch_related('hours', 'hours__survey')

        return queryset


class NoGeoGridTileSerializer(GridTileSerializer):
    """ Serializer excluding polygon field """

    class Meta:
        model = GridTile
        exclude = ('polygon',)
