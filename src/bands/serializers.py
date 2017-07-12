from rest_framework import serializers

from .models import BandCombo

from birds.serializers import BirdSerializer
from birds.models import Bird

class BandComboSerializer(serializers.ModelSerializer):
    bird = BirdSerializer(read_only=True, many=False)

    class Meta:
        model = BandCombo
        fields = '__all__'

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related("bird__bird_extended", "bird__study_area",)

        return queryset
