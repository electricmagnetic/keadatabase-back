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

    class Meta:
        model = Bird
        fields = ('sex', 'status', 'study_area', 'is_extended',)

class BirdViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Bird.objects.all()
    serializer_class = BirdSerializer
    search_fields = ('name',)
    # TODO: ordering
    filter_class = BirdFilter
