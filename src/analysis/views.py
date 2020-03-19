from django.db.models import Count, Case, When, IntegerField
from rest_framework import viewsets

from locations.models import GridTile
from surveys.models import Survey
from .serializers import BaseAnalysisSerializer, GridTileAnalysisSerializer, SurveyAnalysisSerializer

class BaseListSerializerMixin():
    """ For list view return ID only (as detailed calculations too SQL intensive) """
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.serializer_class
        else:
            return BaseAnalysisSerializer


class GridTileAnalysisViewSet(BaseListSerializerMixin, viewsets.ReadOnlyModelViewSet):
    """ Obtain all grid tiles with at least one survey hour """
    queryset = GridTile.objects. \
        prefetch_related('hours'). \
        exclude(hours__isnull=True). \
        annotate(
            all_with_kea=Count(Case(When(hours__kea=True, then=1), output_field=IntegerField())),
            all_total=Count('hours'),
        )

    paginator = None
    serializer_class = GridTileAnalysisSerializer


class SurveyAnalysisViewSet(BaseListSerializerMixin, viewsets.ReadOnlyModelViewSet):
    """ Obtain all surveys """
    queryset = Survey.objects. \
        prefetch_related('hours'). \
        all()
    serializer_class = SurveyAnalysisSerializer
