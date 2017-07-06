from rest_framework import serializers

from .models import StudyArea, Region, CommonLocation

class StudyAreaSerializer(serializers.ModelSerializer):
    birds = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = StudyArea
        fields = '__all__'

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'

class CommonLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommonLocation
        fields = '__all__'
