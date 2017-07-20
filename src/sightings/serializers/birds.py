from rest_framework import serializers
from rest_framework_gis.serializers import GeometryField

from ..models.birds import SightingsBird

class SightingsBirdSerializer(serializers.ModelSerializer):
    get_banded_display = serializers.CharField()
    get_sex_guess_display = serializers.CharField()
    get_life_stage_guess_display = serializers.CharField()

    get_bird_display = serializers.StringRelatedField(source='bird', many=False)
    sighting = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    sighting__date_sighted = serializers.ReadOnlyField(source='sighting.date_sighted')
    sighting__time_sighted = serializers.ReadOnlyField(source='sighting.time_sighted')
    sighting__point_location = GeometryField(source='sighting.point_location')

    class Meta:
        model = SightingsBird
        fields = '__all__'
