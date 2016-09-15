from rest_framework import serializers

from .models import Bird


class BirdSerializer(serializers.HyperlinkedModelSerializer):
    sightings = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Bird
        exclude = ('date_caught', 'caught_by', 'banded_by', 'caught_location', 'health', 'notes',)
