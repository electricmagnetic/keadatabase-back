from rest_framework import serializers

from .models import StudyArea

class StudyAreaSerializer(serializers.ModelSerializer):
    birds = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = StudyArea
        fields = '__all__'
