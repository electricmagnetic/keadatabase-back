from rest_framework import serializers

from .models import StudyArea

class StudyAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyArea
        fields = '__all__'
