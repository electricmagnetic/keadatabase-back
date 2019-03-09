from rest_framework import serializers

from sightings.models.sightings import Sighting, NonSighting
from sightings.models.contributors import Contributor
from sightings.models.birds import BirdSighting

# Helpers
class BirdSightingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BirdSighting
        exclude = ('bird', 'sighting', 'revisit',)

class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = '__all__'

# Report serializers
class ReportBaseSerializer(serializers.ModelSerializer):
    contributor = ContributorSerializer(many=False)
    challenge = serializers.CharField(allow_blank=True, required=False)

    def validate(self, data):
        """ Basic check to deter spam submissions """
        if data.pop('challenge', None) != 'kea':
            raise serializers.ValidationError('Invalid submission')
        return data

class ReportSightingSerializer(ReportBaseSerializer):
    birds = BirdSightingSerializer(many=True)

    class Meta:
        model = Sighting
        exclude = ('quality', 'moderator_notes', 'favourite', 'geocode', 'region', 'import_id',)

    def create(self, validated_data):
        contributor_data = validated_data.pop('contributor')
        birds_data = validated_data.pop('birds')

        contributor = Contributor.objects.create(**contributor_data)
        sighting = Sighting.objects.create(contributor=contributor, **validated_data)

        for bird_data in birds_data:
            BirdSighting.objects.create(sighting=sighting, **bird_data)

        return sighting


class ReportNonSightingSerializer(ReportBaseSerializer):
    class Meta:
        model = NonSighting
        exclude = ('quality', 'moderator_notes', 'region',)

    def create(self, validated_data):
        contributor_data = validated_data.pop('contributor')

        contributor = Contributor.objects.create(**contributor_data)
        non_sighting = NonSighting.objects.create(contributor=contributor,
                                                           **validated_data)

        return non_sighting
