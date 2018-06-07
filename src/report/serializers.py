from rest_framework import serializers

from sightings.models.sightings import SightingsSighting, SightingsNonSighting
from sightings.models.contributors import SightingsContributor
from sightings.models.birds import SightingsBird

# Helpers
class SightingsBirdSerializer(serializers.ModelSerializer):
    class Meta:
        model = SightingsBird
        exclude = ('bird', 'sighting', 'revisit',)

class SightingsContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = SightingsContributor
        fields = '__all__'

# Report serializers
class ReportBaseSerializer(serializers.ModelSerializer):
    contributor = SightingsContributorSerializer(many=False)
    challenge = serializers.CharField(allow_blank=True, required=False)

    def validate(self, data):
        """ Basic check to deter spam submissions """
        if data.pop('challenge', None) != 'kea':
            raise serializers.ValidationError('Invalid submission')
        return data

class ReportSightingSerializer(ReportBaseSerializer):
    birds = SightingsBirdSerializer(many=True)

    class Meta:
        model = SightingsSighting
        exclude = ('quality', 'moderator_notes', 'favourite', 'geocode',)

    def create(self, validated_data):
        contributor_data = validated_data.pop('contributor')
        birds_data = validated_data.pop('birds')

        contributor = SightingsContributor.objects.create(**contributor_data)
        sighting = SightingsSighting.objects.create(contributor=contributor, **validated_data)

        for bird_data in birds_data:
            SightingsBird.objects.create(sighting=sighting, **bird_data)

        return sighting


class ReportNonSightingSerializer(ReportBaseSerializer):
    class Meta:
        model = SightingsNonSighting
        exclude = ('quality', 'moderator_notes',)

    def create(self, validated_data):
        contributor_data = validated_data.pop('contributor')

        contributor = SightingsContributor.objects.create(**contributor_data)
        non_sighting = SightingsNonSighting.objects.create(contributor=contributor,
                                                           **validated_data)

        return non_sighting
