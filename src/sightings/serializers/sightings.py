from rest_framework import serializers

from ..models.sightings import SightingsSighting, SightingsNonSighting

class SightingsBaseSerializer(serializers.ModelSerializer):
    quality = serializers.CharField(source='get_quality_display')

    contributor = serializers.StringRelatedField(many=False)
    region = serializers.StringRelatedField(many=False)

class SightingsSightingSerializer(SightingsBaseSerializer):
    sighting_type = serializers.CharField(source='get_sighting_type_display')
    sighting_birds = serializers.PrimaryKeyRelatedField(source='birds', many=True, read_only=True)

    class Meta:
        model = SightingsSighting
        fields = '__all__'

class SightingsNonSightingSerializer(SightingsBaseSerializer):
    class Meta:
        model = SightingsNonSighting
        fields = '__all__'
