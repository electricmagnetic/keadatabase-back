from rest_framework import viewsets

from ..models.birds import SightingsBird
from ..serializers.birds import SightingsBirdSerializer

class SightingsBirdViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SightingsBird.objects. \
               select_related('sighting', 'bird',). \
               all()
    serializer_class = SightingsBirdSerializer
    ordering = ('-sighting__date_sighted', '-sighting__time_sighted',)
    ordering_fields = ('id', 'banded', 'sighting', 'sighting__date_sighted',
                       'sighting__time_sighted', 'bird',)
    filter_fields = ('sighting', 'bird',)
