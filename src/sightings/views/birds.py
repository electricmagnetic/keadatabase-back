import django_filters
from rest_framework import viewsets

from keadatabase.pagination import ObservationPagination
from ..models.birds import BirdSighting
from ..serializers.birds import BirdObservationSerializer

class BirdSightingFilter(django_filters.FilterSet):
    has_bird = django_filters.BooleanFilter(field_name='bird',
                                            lookup_expr='isnull',
                                            exclude=True,
                                            label='Has bird')

    class Meta:
        model = BirdSighting
        fields = ('sighting', 'bird',)

class BirdObservationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BirdObservationSerializer
    pagination_class = ObservationPagination
    ordering = ('-sighting__date_sighted', '-sighting__time_sighted',)
    ordering_fields = ('id', 'banded', 'sighting', 'sighting__date_sighted',
                       'sighting__time_sighted', 'bird',)
    filter_class = BirdSightingFilter

    def get_queryset(self):
        queryset = BirdSighting.objects.exclude(sighting__status='private').exclude(sighting__status='bad')

        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset
