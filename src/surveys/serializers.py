from rest_framework import serializers

from .models.surveys import Survey

class SurveySerializer(serializers.ModelSerializer):
    get_status_display = serializers.CharField()
    observer = serializers.StringRelatedField(many=False)

    class Meta:
        model = Survey
        fields = '__all__'
