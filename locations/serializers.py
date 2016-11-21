from rest_framework import serializers

from .models import PrimaryLocation, SecondaryLocation, HomeLocation


class PrimaryLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrimaryLocation
        fields = '__all__'


class SecondaryLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecondaryLocation
        fields = '__all__'


class HomeLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeLocation
        fields = '__all__'
