from rest_framework import serializers

from .models import Band


class BandSerializer(serializers.ModelSerializer):
    # Choices
    #band_type = serializers.CharField(source='get_band_type_display')
    #band_symbol_colour = serializers.CharField(
    #    source='get_band_symbol_colour_display'
    #)
    #band_colour = serializers.CharField(source='get_band_colour_display')


    # Methods
    #get_colour_band = serializers.ReadOnlyField()
    #get_colour_band_code = serializers.ReadOnlyField()


    # Relations
    #bird = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = Band
        fields = '__all__'
