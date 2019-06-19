from rest_framework import viewsets

from keadatabase.pagination import SightingPagination
from ..models.media import SightingsMedia
from ..serializers.media import SightingsMediaSerializer

class SightingsMediaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SightingsMedia.objects. \
               select_related('sighting'). \
               prefetch_related('birds'). \
               all()
    serializer_class = SightingsMediaSerializer
    pagination_class = SightingPagination
    ordering_fields = ('id', 'sighting',)
    filter_fields = ('id', 'sighting', 'birds',)
    # filter_fields
