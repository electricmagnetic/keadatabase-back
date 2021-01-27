from rest_framework import viewsets

from keadatabase.pagination import ObservationPagination
from ..models.observations import Sighting
from ..serializers.observations import ObservationSerializer


class ObservationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Sighting.objects. \
               select_related('contributor',). \
               exclude(status='private').exclude(status='bad')
    serializer_class = ObservationSerializer
    pagination_class = ObservationPagination
    filter_fields = (
        'sighting_type',
        'precision',
        'number',
        'status',
        'confirmed',
    )
    ordering_fields = (
        'contributor',
        'region',
        'date_sighted',
        'time_sighted',
        'date_created',
        'date_updated',
    )
