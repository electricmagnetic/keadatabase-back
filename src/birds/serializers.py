from rest_framework import serializers
from versatileimagefield.serializers import VersatileImageFieldSerializer

from .models import Bird, BirdExtended

class BirdExtendedSerializer(serializers.ModelSerializer):
    profile_picture = VersatileImageFieldSerializer(
        sizes='profile_picture'
    )

    class Meta:
        model = BirdExtended
        fields = ('description', 'is_featured', 'sponsor_name',
                  'sponsor_website', 'profile_picture', 'profile_picture_attribution',)

class BirdSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display')
    sex = serializers.CharField(source='get_sex_display')

    bird_extended = BirdExtendedSerializer()

    get_age = serializers.ReadOnlyField()
    get_life_stage = serializers.ReadOnlyField()

    study_area = serializers.StringRelatedField(many=False)
    band_combo = serializers.StringRelatedField(many=False)

    class Meta:
        model = Bird
        fields = '__all__'

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related("bird_extended", "study_area", "band_combo")

        return queryset
