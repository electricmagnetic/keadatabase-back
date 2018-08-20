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
    serializer_class = SightingsBirdSerializer
    pagination_class = SightingPagination
    ordering = ('-sighting__date_sighted', '-sighting__time_sighted',)
    ordering_fields = ('id', 'banded', 'sighting', 'sighting__date_sighted',
                       'sighting__time_sighted', 'bird',)
    filter_class = SightingsBirdFilter

    def get_queryset(self):
        queryset = SightingsBird.objects.all()

        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset
