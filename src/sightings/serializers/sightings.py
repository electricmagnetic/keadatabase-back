from rest_framework import serializers

from ..models.sightings import SightingsSighting, SightingsNonSighting

class SightingsNonSightingSerializer(serializers.ModelSerializer):
    contributor = serializers.StringRelatedField(many=False)
    quality = serializers.CharField(source='get_quality_display')
    region = serializers.StringRelatedField(many=False)

    class Meta:
        model = SightingsNonSighting
        fields = '__all__'
