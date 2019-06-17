from rest_framework import viewsets

from keadatabase.pagination import SurveyPagination
from .models.surveys import Survey
from .serializers import SurveySerializer

class SurveyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Survey.objects. \
               all()
    serializer_class = SurveySerializer
    pagination_class = SurveyPagination
    ordering = ('-date',)
    ordering_fields = ('id', 'date',)
    filter_fields = ('status',)
