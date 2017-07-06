from rest_framework import viewsets

from .models import StudyArea, Region
from .serializers import StudyAreaSerializer, RegionSerializer

class StudyAreaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StudyArea.objects. \
               prefetch_related('birds'). \
               all()
    serializer_class = StudyAreaSerializer
    search_fields = ('name',)
    ordering_fields = ('name',)

class RegionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    search_fields = ('name',)
    ordering_fields = ('name',)
