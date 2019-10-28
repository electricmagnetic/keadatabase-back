from django.db.models.functions import TruncQuarter
from django.db.models import Count
from rest_framework import serializers

from locations.models import GridTile
from surveys.models.surveys import Survey

class BaseAnalysisSerializer(serializers.Serializer):
    """ Basic list only analysis serializer """
    id = serializers.CharField()

class GridTileAnalysisSerializer(BaseAnalysisSerializer):
    """ Perform basic queries to provide an endpoint with grid tile analysis """

    hours_total = serializers.SerializerMethodField()
    hours_with_kea = serializers.SerializerMethodField()
    hours_per_quarter = serializers.SerializerMethodField()

    def get_hours_total(self, instance):
        return instance.hours.count()

    def get_hours_with_kea(self, instance):
        return instance.hours.filter(kea=True).count()

    def get_hours_per_quarter(self, instance):
        return instance.hours \
                .annotate(quarter=TruncQuarter('survey__date')) \
                .values('quarter') \
                .annotate(count=Count('id')) \
                .order_by()

class SurveyAnalysisSerializer(BaseAnalysisSerializer):
    """ Perform basic queries to provide an endpoint with survey analysis """

    hours_surveyed = serializers.SerializerMethodField()
    hours_with_kea = serializers.SerializerMethodField()

    def get_hours_surveyed(self, instance):
        return instance.hours.exclude(activity='X').count()

    def get_hours_with_kea(self, instance):
        return instance.hours.filter(kea=True).count()
