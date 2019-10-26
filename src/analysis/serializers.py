from rest_framework import serializers

from locations.models import GridTile

class GridTileAnalysisSerializer(serializers.Serializer):
    """ Perform basic queries to provide an endpoint with grid tile analysis """

    id = serializers.CharField()
    hours_total = serializers.SerializerMethodField(method_name='get_hours_total')
    hours_with_kea = serializers.SerializerMethodField(method_name='get_hours_with_kea')

    class Meta:
        model = GridTile

    def get_hours_total(self, instance):
        return instance.hours.count()

    def get_hours_with_kea(self, instance):
        return instance.hours.filter(kea=True).count()
