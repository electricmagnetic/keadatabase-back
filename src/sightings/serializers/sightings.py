from rest_framework import serializers

from ..models.sightings import SightingsSighting, SightingsNonSighting

class SightingsBaseSerializer(serializers.ModelSerializer):
    get_quality_display = serializers.CharField()

    contributor = serializers.StringRelatedField(many=False)
    region = serializers.StringRelatedField(many=False)

class SightingsSightingSerializer(SightingsBaseSerializer):
    get_sighting_type_display = serializers.CharField()

    class Meta:
        model = SightingsSighting
        fields = '__all__'

class SightingsNonSightingSerializer(SightingsBaseSerializer):
    class Meta:
        model = SightingsNonSighting
        fields = '__all__'
