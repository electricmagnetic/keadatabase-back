from rest_framework import serializers

from .models.surveys import Survey, SurveyHour

class SurveyHourSerializer(serializers.ModelSerializer):
    get_activity_display = serializers.CharField()
    get_hour_display = serializers.ReadOnlyField()

    class Meta:
        model = SurveyHour
        fields = '__all__'

class SurveySerializer(serializers.ModelSerializer):
    get_status_display = serializers.CharField()
    observer = serializers.StringRelatedField(many=False)

    hours = SurveyHourSerializer(many=True)

    class Meta:
        model = Survey
        fields = '__all__'
