from rest_framework import serializers

from ..models.observations import Sighting


class ObservationSerializer(serializers.ModelSerializer):
    contributor = serializers.StringRelatedField(many=False)
    get_status_display = serializers.CharField()
    get_sighting_type_display = serializers.CharField()

    class Meta:
        model = Sighting
        exclude = (
            'moderator_notes',
            'import_id',
        )
