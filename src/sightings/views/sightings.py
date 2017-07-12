from rest_framework import viewsets

from ..models.sightings import SightingsSighting, SightingsNonSighting
from ..serializers.sightings import SightingsNonSightingSerializer

class SightingsNonSightingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SightingsNonSighting.objects. \
               select_related('contributor', 'region'). \
               all()
    serializer_class = SightingsNonSightingSerializer
    ordering_fields = ('contributor', 'quality', 'region', 'date_sighted', 'time_sighted',
                       'date_created', 'date_updated',)
    filter_fields = ('quality', 'region',)
