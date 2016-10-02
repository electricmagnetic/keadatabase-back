from rest_framework import serializers

from .models import Bird, BirdSighting


class BirdSerializer(serializers.HyperlinkedModelSerializer):
    # Choices
    status = serializers.CharField(source='get_status_display')
    sex = serializers.CharField(source='get_sex_display')
    life_stage = serializers.CharField(source='get_life_stage_display')
    id_band_leg = serializers.CharField(source='get_id_band_leg_display')


    # Methods
    get_identifier = serializers.ReadOnlyField()


    # Relations
    sightings = serializers.HyperlinkedRelatedField(many=True, read_only=True,
                                                    view_name='birdsighting-detail')


    class Meta:
        model = Bird
        exclude = ('date_caught', 'caught_by', 'banded_by', 'caught_location',
                   'transmitter_channel', 'notes',)


class BirdSightingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BirdSighting
        exclude = ('verification',)
