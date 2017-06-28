import django_filters
from rest_framework import viewsets

from .models import Bird
from .serializers import BirdSerializer

class BirdFilter(django_filters.FilterSet):
    is_extended = django_filters.BooleanFilter(name='bird_extended__is_extended',
                                               lookup_expr='isnull',
                                               exclude=True,
                                               label='Is extended')
    is_featured = django_filters.BooleanFilter(name='bird_extended__is_featured',
                                               label='Is featured')

    has_band = django_filters.BooleanFilter(name='band_combo', lookup_expr='isnull', exclude=True)

    class Meta:
        model = Bird
        fields = ('sex', 'status', 'study_area', 'is_extended',)

class BirdViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Bird.objects. \
               select_related('bird_extended', 'band_combo', 'study_area',). \
               all()
    serializer_class = BirdSerializer
    search_fields = ('name',)
    ordering_fields = ('name', 'status', 'study_area', 'bird_extended',)
    filter_class = BirdFilter
