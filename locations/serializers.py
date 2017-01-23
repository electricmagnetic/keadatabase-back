from rest_framework import serializers

from .models import PrimaryLocation, SecondaryLocation, AreaLocation


class PrimaryLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrimaryLocation
        fields = '__all__'


class SecondaryLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecondaryLocation
        fields = '__all__'


class AreaLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreaLocation
        fields = '__all__'
