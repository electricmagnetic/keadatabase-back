from rest_framework import serializers

from ..models.birds import SightingsBird

class SightingsBirdSerializer(serializers.ModelSerializer):
    banded = serializers.CharField(source='get_banded_display')
    sex_guess = serializers.CharField(source='get_sex_guess_display')
    life_stage_guess = serializers.CharField(source='get_life_stage_guess_display')

    get_bird_display = serializers.StringRelatedField(source='bird', many=False)
    sighting = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    sighting__date_sighted = serializers.ReadOnlyField(source='sighting.date_sighted')
    sighting__time_sighted = serializers.ReadOnlyField(source='sighting.time_sighted')

    class Meta:
        model = SightingsBird
        fields = '__all__'
