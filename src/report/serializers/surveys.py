from rest_framework import serializers

from surveys.models.surveys import Survey, SurveyHour
from surveys.models.observers import Observer

# Helpers
class SurveyHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyHour
        exclude = ('survey',)

class ObserverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Observer
        fields = '__all__'

# Report serializers
class ReportSurveySerializer(serializers.ModelSerializer):
    hours = SurveyHourSerializer(many=True)
    observer = ObserverSerializer(many=False)
    challenge = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = Survey
        exclude = ('status',)

    def to_internal_value(self, data):
        """ Set both empty strings and 0 to null for max_flock_size """
        if data.get('max_flock_size', None) == '': data.pop('max_flock_size')
        if data.get('max_flock_size', None) == 0: data.pop('max_flock_size')
        return super().to_internal_value(data)

    def create(self, validated_data):
        observer_data = validated_data.pop('observer')
        hours_data = validated_data.pop('hours')

        observer = Observer.objects.create(**observer_data)
        survey = Survey.objects.create(observer=observer, **validated_data)

        for hour_data in hours_data:
            SurveyHour.objects.create(survey=survey, **hour_data)

        return survey

    def validate(self, data):
        """ Basic check to deter spam submissions """
        if data.pop('challenge', None) != 'kea':
            raise serializers.ValidationError('Invalid submission')
        return data
