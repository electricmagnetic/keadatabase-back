from rest_framework import viewsets

from keadatabase.pagination import SurveyPagination
from .models.surveys import Survey, SurveyHour
from .serializers import SurveySerializer, SurveyHourSerializer

class SurveyHourViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SurveyHourSerializer
    pagination_class = SurveyPagination
    ordering = ('-survey__date',)
    ordering_fields = ('id', 'survey__date',)
    filter_fields = ('grid_tile', 'activity', 'kea', 'survey',)

    def get_queryset(self):
        queryset = SurveyHour.objects. \
                   select_related('survey', 'grid_tile'). \
                   all()

        return queryset

class SurveyViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SurveySerializer
    pagination_class = SurveyPagination
    ordering = ('-date',)
    ordering_fields = ('id', 'date',)
    filter_fields = ('status',)

    def get_queryset(self):
        queryset = Survey.objects. \
                   prefetch_related('hours'). \
                   select_related('observer'). \
                   all()

        return queryset
