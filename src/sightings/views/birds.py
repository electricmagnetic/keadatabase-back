import django_filters
from rest_framework import viewsets

from keadatabase.pagination import SightingPagination
from ..models.birds import BirdSighting
from ..serializers.birds import BirdSightingSerializer

class BirdSightingFilter(django_filters.FilterSet):
    has_bird = django_filters.BooleanFilter(field_name='bird',
                                            lookup_expr='isnull',
                                            exclude=True,
                                            label='Has bird')

    class Meta:
        model = BirdSighting
        fields = ('sighting', 'bird',)

class BirdSightingViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BirdSightingSerializer
    pagination_class = SightingPagination
    ordering = ('-sighting__date_sighted', '-sighting__time_sighted',)
    ordering_fields = ('id', 'banded', 'sighting', 'sighting__date_sighted',
                       'sighting__time_sighted', 'bird',)
    filter_class = BirdSightingFilter

    def get_queryset(self):
        queryset = BirdSighting.objects.all()

        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset
