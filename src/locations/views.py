from rest_framework import viewsets

from .models import StudyArea
from .serializers import StudyAreaSerializer

class StudyAreaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StudyArea.objects.all()
    serializer_class = StudyAreaSerializer
    filter_fields = ('name',)
