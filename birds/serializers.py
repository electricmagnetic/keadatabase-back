from rest_framework import serializers

from .models import Bird, BirdSighting


class BirdSerializer(serializers.HyperlinkedModelSerializer):
    #id = serializers.ReadOnlyField()
    sightings = serializers.HyperlinkedRelatedField(many=True, read_only=True,
                                                    view_name='birdsighting-detail')
    get_identifier = serializers.ReadOnlyField()


    class Meta:
        model = Bird
        exclude = ('date_caught', 'caught_by', 'banded_by', 'caught_location',
                   'transmitter_channel', 'notes',)


class BirdSightingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BirdSighting
        exclude = ('verification',)
