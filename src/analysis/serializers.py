from django.db.models.functions import TruncQuarter
from django.db.models import Count, Q
from rest_framework import serializers

from locations.models import GridTile
from surveys.models.surveys import Survey

class BaseAnalysisSerializer(serializers.Serializer):
    """ Basic list only analysis serializer """
    id = serializers.CharField()

    all_with_kea = serializers.IntegerField()
    all_total = serializers.IntegerField()

class GridTileAnalysisSerializer(BaseAnalysisSerializer):
    """ Perform basic queries to provide an endpoint with grid tile analysis """

    per_quarter = serializers.SerializerMethodField()

    def get_per_quarter(self, instance):
        return instance.hours. \
                annotate(quarter=TruncQuarter('survey__date')). \
                values('quarter'). \
                annotate(total=Count('id'), with_kea=Count('id', filter=Q(kea=True))). \
                order_by()

class SurveyAnalysisSerializer(BaseAnalysisSerializer):
    """ Perform basic queries to provide an endpoint with survey analysis """

    hours_total = serializers.SerializerMethodField()

    def get_hours_total(self, instance):
        return instance.hours. \
            aggregate(surveyed=Count('id', filter=~Q(activity='X')), with_kea=Count('id', filter=Q(kea=True)))
