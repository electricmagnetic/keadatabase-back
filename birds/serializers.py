from rest_framework import serializers

from .models import Bird, BirdSighting


class BirdSerializer(serializers.ModelSerializer):
    # Choices
    status = serializers.CharField(source='get_status_display')
    sex = serializers.CharField(source='get_sex_display')


    # Methods
    get_age = serializers.ReadOnlyField()
    get_life_stage = serializers.ReadOnlyField()


    # Relations
    #sightings = serializers.PrimaryKeyRelatedField(many=True, read_only=True)


    class Meta:
        model = Bird
        exclude = ('date_imported',)


class BirdSightingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BirdSighting
        exclude = ('verification',)
