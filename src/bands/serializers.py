from rest_framework import serializers

from birds.serializers import BirdSerializer
from .models import BandCombo

class BandComboSerializer(serializers.ModelSerializer):
    bird_name = serializers.ReadOnlyField(source='bird.name')

    class Meta:
        model = BandCombo
        fields = '__all__'
