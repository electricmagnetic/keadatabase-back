from rest_framework import viewsets

from keadatabase.pagination import LocationPagination
from .models import StudyArea, Region
from .serializers import StudyAreaSerializer, RegionSerializer

class StudyAreaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StudyArea.objects. \
               prefetch_related('birds'). \
               all()
    serializer_class = StudyAreaSerializer
    pagination_class = LocationPagination
    search_fields = ('name',)
    ordering_fields = ('name',)

class RegionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Region.objects. \
               prefetch_related('study_areas'). \
               all()
    serializer_class = RegionSerializer
    pagination_class = LocationPagination
    search_fields = ('name',)
    ordering_fields = ('name',)
