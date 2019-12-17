from rest_framework import viewsets

from keadatabase.pagination import SightingPagination
from ..models.sightings import Sighting
from ..serializers.sightings import SightingSerializer

class SightingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Sighting.objects. \
               select_related('contributor',). \
               exclude(status='private').exclude(status='bad')
    serializer_class = SightingSerializer
    pagination_class = SightingPagination
    filter_fields = ('sighting_type', 'precision', 'number', 'status', 'confirmed',)
    ordering_fields = ('contributor', 'region', 'date_sighted', 'time_sighted',
                       'date_created', 'date_updated',)
