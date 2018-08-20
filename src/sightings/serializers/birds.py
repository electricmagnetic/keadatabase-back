from rest_framework import serializers
from rest_framework_gis.serializers import GeometryField

from ..models.birds import SightingsBird
from birds.serializers import BirdSerializer

class SightingsBirdSerializer(serializers.ModelSerializer):
    get_banded_display = serializers.CharField()
    get_sex_guess_display = serializers.CharField()
    get_life_stage_guess_display = serializers.CharField()

    bird = BirdSerializer(many=False, read_only=True)
    sighting = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    sighting__date_sighted = serializers.ReadOnlyField(source='sighting.date_sighted')
    sighting__time_sighted = serializers.ReadOnlyField(source='sighting.time_sighted')
    sighting__point_location = GeometryField(source='sighting.point_location')

    class Meta:
        model = SightingsBird
        fields = '__all__'

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.prefetch_related("bird", "bird__band_combo", "bird__study_area", "bird__bird_extended", "sighting",)

        return queryset
