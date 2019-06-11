import django_filters
from rest_framework import viewsets

from keadatabase.pagination import BirdPagination
from .models import Bird
from .serializers import BirdSerializer

EMPTY_VALUES = ([], (), {}, '', None)

class BirdOrdering(django_filters.OrderingFilter):
    def __init__(self, *args, **kwargs):
        super(BirdOrdering, self).__init__(*args, **kwargs)
        self.extra['choices'] += [
            ('random', 'Random')
        ]

    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs
        if any(v in ['random'] for v in value):
            return qs.order_by('?')

        return super(BirdOrdering, self).filter(qs, value)

class BirdFilter(django_filters.FilterSet):
    is_extended = django_filters.BooleanFilter(field_name='bird_extended__is_extended',
                                               lookup_expr='isnull',
                                               exclude=True,
                                               label='Is extended')
    is_featured = django_filters.BooleanFilter(field_name='bird_extended__is_featured',
                                               label='Is featured')

    has_band = django_filters.BooleanFilter(field_name='band_combo', lookup_expr='isnull', exclude=True)

    ordering = BirdOrdering(fields=('name', 'status', 'study_area', 'bird_extended', 'date_imported',))

    class Meta:
        model = Bird
        fields = ('sex', 'status', 'study_area', 'is_extended',)

class BirdViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Bird.objects. \
               select_related('bird_extended', 'band_combo', 'study_area',). \
               all()
    serializer_class = BirdSerializer
    pagination_class = BirdPagination
    search_fields = ('name',)
    ordering_fields = ('name', 'status', 'study_area', 'bird_extended', 'date_imported',)
    filter_class = BirdFilter
