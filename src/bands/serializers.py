from rest_framework import serializers

from .models import BandCombo

class BandComboSerializer(serializers.ModelSerializer):
    class Meta:
        model = BandCombo
        fields = '__all__'
