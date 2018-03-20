import django_filters
from rest_framework import viewsets

from keadatabase.pagination import SightingPagination
from ..models.birds import SightingsBird
from ..serializers.birds import SightingsBirdSerializer

class SightingsBirdFilter(django_filters.FilterSet):
    has_bird = django_filters.BooleanFilter(name='bird',
                                            lookup_expr='isnull',
                                            exclude=True,
                                            label='Has bird')

    class Meta:
        model = SightingsBird
        fields = ('sighting', 'bird',)

class SightingsBirdViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SightingsBird.objects. \
               select_related('sighting', 'bird',). \
               all()
    serializer_class = SightingsBirdSerializer
    pagination_class = SightingPagination
    ordering = ('-sighting__date_sighted', '-sighting__time_sighted',)
    ordering_fields = ('id', 'banded', 'sighting', 'sighting__date_sighted',
                       'sighting__time_sighted', 'bird',)
    filter_class = SightingsBirdFilter
