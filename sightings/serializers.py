from rest_framework import serializers

from .models import Sighting


class SightingSerializer(serializers.ModelSerializer):
    birds = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Sighting
        exclude = ('email', 'phone', 'newsletter',)
