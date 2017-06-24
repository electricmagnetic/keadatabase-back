from rest_framework import serializers

from .models import Bird

class BirdSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display')
    sex = serializers.CharField(source='get_sex_display')
    study_area = serializers.StringRelatedField(many=False)
    band_combo = serializers.StringRelatedField(many=False)

    get_age = serializers.ReadOnlyField()
    get_life_stage = serializers.ReadOnlyField()

    class Meta:
        model = Bird
        fields = '__all__'
