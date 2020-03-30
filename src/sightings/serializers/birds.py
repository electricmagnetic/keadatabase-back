from rest_framework import serializers
from rest_framework_gis.serializers import GeometryField

from ..models.birds import BirdSighting
from .sightings import SightingSerializer
from birds.serializers import BirdSerializer

class BirdSightingSerializer(serializers.ModelSerializer):
    get_banded_display = serializers.CharField()
    get_sex_guess_display = serializers.CharField()
    get_life_stage_guess_display = serializers.CharField()

    bird = BirdSerializer(many=False, read_only=True)
    sighting = SightingSerializer(many=False, read_only=True)

    # TODO: remove these three fields. Currently left in for backwards compatibility.
    sighting__date_sighted = serializers.ReadOnlyField(source='sighting.date_sighted')
    sighting__time_sighted = serializers.ReadOnlyField(source='sighting.time_sighted')
    sighting__point_location = GeometryField(source='sighting.point_location')

    class Meta:
        model = BirdSighting
        fields = '__all__'

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.prefetch_related(
            "bird",
            "bird__band_combo",
            "bird__study_area",
            "bird__bird_extended",
            "sighting",
            "sighting__contributor",
        )

        return queryset
