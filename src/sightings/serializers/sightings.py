from rest_framework import serializers

from ..models.sightings import SightingsSighting, SightingsNonSighting

class SightingsBaseSerializer(serializers.ModelSerializer):
    get_quality_display = serializers.CharField()

    contributor = serializers.StringRelatedField(many=False)
    region = serializers.StringRelatedField(many=False)

class SightingsSightingSerializer(SightingsBaseSerializer):
    get_sighting_type_display = serializers.CharField()
    sighting_birds = serializers.PrimaryKeyRelatedField(source='birds', many=True, read_only=True)

    class Meta:
        model = SightingsSighting
        fields = '__all__'

class SightingsNonSightingSerializer(SightingsBaseSerializer):
    class Meta:
        model = SightingsNonSighting
        fields = '__all__'
