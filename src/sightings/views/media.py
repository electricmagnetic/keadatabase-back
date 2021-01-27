from rest_framework import viewsets

from keadatabase.pagination import ObservationPagination
from ..models.media import SightingsMedia
from ..serializers.media import ObservationsMediaSerializer


class ObservationsMediaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SightingsMedia.objects. \
               select_related('sighting'). \
               prefetch_related('birds'). \
               all()
    serializer_class = ObservationsMediaSerializer
    pagination_class = ObservationPagination
    ordering_fields = (
        'id',
        'sighting',
    )
    filter_fields = (
        'id',
        'sighting',
        'birds',
    )
    # filter_fields
