from rest_framework import viewsets

from keadatabase.pagination import SightingPagination
from ..models.sightings import SightingsSighting, SightingsNonSighting
from ..serializers.sightings import SightingsSightingSerializer, SightingsNonSightingSerializer

class SightingsBaseViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = SightingPagination
    ordering_fields = ('contributor', 'quality', 'region', 'date_sighted', 'time_sighted',
                       'date_created', 'date_updated',)

class SightingsSightingViewSet(SightingsBaseViewSet):
    queryset = SightingsSighting.objects. \
               select_related('contributor', 'region',). \
               all()
    serializer_class = SightingsSightingSerializer
    filter_fields = ('quality', 'region', 'sighting_type', 'accuracy', 'specificity', 'number',)

class SightingsNonSightingViewSet(SightingsBaseViewSet):
    queryset = SightingsNonSighting.objects. \
               select_related('contributor', 'region',). \
               all()
    serializer_class = SightingsNonSightingSerializer
    filter_fields = ('quality', 'region',)
