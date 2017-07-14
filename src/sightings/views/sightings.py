from rest_framework import viewsets

from keadatabase.pagination import SightingPagination
from ..models.sightings import SightingsSighting, SightingsNonSighting
from ..serializers.sightings import SightingsSightingSerializer, SightingsNonSightingSerializer

class SightingsSightingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SightingsSighting.objects. \
               select_related('contributor', 'region',). \
               prefetch_related('birds'). \
               all()
    serializer_class = SightingsSightingSerializer
    pagination_class = SightingPagination
    # ordering_fields
    # filter_fields

class SightingsNonSightingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SightingsNonSighting.objects. \
               select_related('contributor', 'region',). \
               all()
    serializer_class = SightingsNonSightingSerializer
    pagination_class = SightingPagination
    ordering_fields = ('contributor', 'quality', 'region', 'date_sighted', 'time_sighted',
                       'date_created', 'date_updated',)
    filter_fields = ('quality', 'region',)
