from rest_framework import serializers

from ..models.sightings import Sighting

class SightingSerializer(serializers.ModelSerializer):
    contributor = serializers.StringRelatedField(many=False)
    get_status_display = serializers.CharField()
    get_sighting_type_display = serializers.CharField()

    class Meta:
        model = Sighting
        exclude = ('moderator_notes', 'import_id',)
