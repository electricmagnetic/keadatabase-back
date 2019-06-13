from rest_framework import serializers

from .models import GridTile

class GridTileSerializer(serializers.ModelSerializer):
    class Meta:
        model = GridTile
        fields = '__all__'
