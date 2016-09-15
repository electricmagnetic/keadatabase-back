from rest_framework import serializers

from .models import Sighting


class SightingSerializer(serializers.HyperlinkedModelSerializer):
    birds = serializers.HyperlinkedRelatedField(many=True, read_only=True,
                                                view_name='birdsighting-detail')

    class Meta:
        model = Sighting
        exclude = ('email', 'phone', 'newsletter',)
