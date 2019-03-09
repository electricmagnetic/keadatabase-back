from rest_framework import serializers

from ..models.sightings import Sighting, NonSighting

class BaseSightingSerializer(serializers.ModelSerializer):
    get_status_display = serializers.CharField()

    contributor = serializers.StringRelatedField(many=False)

class SightingSerializer(BaseSightingSerializer):
    get_sighting_type_display = serializers.CharField()

    class Meta:
        model = Sighting
        exclude = ('moderator_notes', 'import_id',)

class NonSightingSerializer(BaseSightingSerializer):
    class Meta:
        model = NonSighting
        exclude = ('moderator_notes', )
