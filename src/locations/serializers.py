from rest_framework import serializers

from .models import StudyArea, Region

class StudyAreaSerializer(serializers.ModelSerializer):
    birds = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = StudyArea
        fields = '__all__'

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'
