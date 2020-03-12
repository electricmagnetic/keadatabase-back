from rest_framework import viewsets, permissions

from keadatabase.pagination import SurveyPagination
from .models.surveys import Survey, SurveyHour
from .models.observers import Observer
from .serializers import SurveySerializer, SurveyHourSerializer, ObserverSerializer

class SurveyHourViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SurveyHourSerializer
    pagination_class = SurveyPagination
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
    ordering_fields = ('id', 'date',)
    filter_fields = ('status',)

    def get_queryset(self):
        queryset = Survey.objects. \
                   prefetch_related('hours'). \
                   select_related('observer'). \
                   all()

        return queryset

class ObserverViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ObserverSerializer
    pagination_class = SurveyPagination
    ordering_fields = ('name',)
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Observer.objects. \
                   select_related('survey'). \
                   all()

        return queryset
