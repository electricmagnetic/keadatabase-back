from rest_framework import serializers

from .models import Band


class BandSerializer(serializers.HyperlinkedModelSerializer):
    bird = serializers.HyperlinkedRelatedField(many=False, read_only=True,
                                               view_name='bird-detail')

    class Meta:
        model = Band
        fields = '__all__'
