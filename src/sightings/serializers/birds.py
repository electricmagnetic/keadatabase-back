from rest_framework import serializers

from ..models.birds import SightingsBird

class SightingsBirdSerializer(serializers.ModelSerializer):
    get_banded_display = serializers.CharField()
    get_sex_guess_display = serializers.CharField()
    get_life_stage_guess_display = serializers.CharField()

    get_bird_display = serializers.StringRelatedField(source='bird', many=False)
    sighting = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    sighting__date_sighted = serializers.ReadOnlyField(source='sighting.date_sighted')
    sighting__time_sighted = serializers.ReadOnlyField(source='sighting.time_sighted')

    class Meta:
        model = SightingsBird
        fields = '__all__'
