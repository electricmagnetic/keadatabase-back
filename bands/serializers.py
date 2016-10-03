from rest_framework import serializers

from .models import Band


class BandSerializer(serializers.HyperlinkedModelSerializer):
    # Choices
    colour_band_type = serializers.CharField(source='get_colour_band_type_display')
    colour_band_symbol_colour = serializers.CharField(
        source='get_colour_band_symbol_colour_display'
    )
    colour_band_colour = serializers.CharField(source='get_colour_band_colour_display')


    # Methods
    get_colour_band_code = serializers.ReadOnlyField()


    # Relations
    bird = serializers.HyperlinkedRelatedField(many=False, read_only=True,
                                               view_name='bird-detail')

    class Meta:
        model = Band
        fields = '__all__'
