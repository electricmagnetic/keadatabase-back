from rest_framework import serializers

from .models import PrimaryLocation, SecondaryLocation


class PrimaryLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrimaryLocation
        fields = '__all__'


class SecondaryLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecondaryLocation
        fields = '__all__'
