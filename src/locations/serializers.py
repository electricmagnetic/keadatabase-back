from rest_framework import serializers

from .models import GridTile
from surveys.serializers import SurveyHourSerializer

class GridTileSerializer(serializers.ModelSerializer):
    get_image = serializers.ReadOnlyField()
    hours = SurveyHourSerializer(many=True)

    class Meta:
        model = GridTile
        fields = '__all__'
