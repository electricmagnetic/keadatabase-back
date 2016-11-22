from rest_framework import serializers

from .models import Band


class BandSerializer(serializers.ModelSerializer):
    """ Serializer for Band functions and fields """

    # Choices
    get_style_display = serializers.ReadOnlyField()
    get_size_display = serializers.ReadOnlyField()
    get_colour_display = serializers.ReadOnlyField()
    get_position_display =  serializers.ReadOnlyField()
    get_leg_display = serializers.ReadOnlyField()
    get_symbol_display = serializers.ReadOnlyField()
    get_symbol_colour_display  = serializers.ReadOnlyField()


    # Methods
    get_bird_display = serializers.ReadOnlyField()
    get_band_type = serializers.ReadOnlyField()
    get_band_type_display = serializers.ReadOnlyField()
    get_band_combo_display = serializers.ReadOnlyField()
    get_str = serializers.ReadOnlyField(source='__str__', read_only=True)


    # Meta
    class Meta:
        model = Band
        fields = '__all__'
