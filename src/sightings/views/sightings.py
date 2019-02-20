from rest_framework import viewsets

from keadatabase.pagination import SightingPagination
from ..models.sightings import Sighting, NonSighting
from ..serializers.sightings import SightingSerializer, NonSightingSerializer

class BaseSightingViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = SightingPagination
    ordering_fields = ('contributor', 'quality', 'region', 'date_sighted', 'time_sighted',
                       'date_created', 'date_updated',)

class SightingViewSet(BaseSightingViewSet):
    queryset = Sighting.objects. \
               select_related('contributor',). \
               all()
    serializer_class = SightingSerializer
    filter_fields = ('quality', 'sighting_type', 'precision', 'number',)

class NonSightingViewSet(BaseSightingViewSet):
    queryset = NonSighting.objects. \
               select_related('contributor',). \
               all()
    serializer_class = NonSightingSerializer
    filter_fields = ('quality', 'region',)
