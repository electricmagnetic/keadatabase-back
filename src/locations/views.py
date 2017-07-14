from rest_framework import viewsets

from .models import StudyArea, Region, CommonLocation
from .serializers import StudyAreaSerializer, RegionSerializer, CommonLocationSerializer

class StudyAreaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StudyArea.objects. \
               prefetch_related('birds'). \
               all()
    serializer_class = StudyAreaSerializer
    search_fields = ('name',)
    ordering_fields = ('name',)

class RegionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Region.objects. \
               prefetch_related('study_areas'). \
               all()
    serializer_class = RegionSerializer
    search_fields = ('name',)
    ordering_fields = ('name',)

class CommonLocationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CommonLocation.objects.all()
    serializer_class = CommonLocationSerializer
    search_fields = ('name',)
    filter_fields = ('specificity',)
    ordering_fields = ('name',)
