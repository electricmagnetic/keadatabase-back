import django_filters
from rest_framework import viewsets

from .models import BandCombo
from .serializers import BandComboSerializer

class BandComboFilter(django_filters.FilterSet):
    colours = django_filters.BaseInFilter(lookup_expr='contains')
    symbols = django_filters.BaseInFilter(lookup_expr='contains')

    is_extended = django_filters.BooleanFilter(name='bird__bird_extended__is_extended',
                                               lookup_expr='isnull',
                                               exclude=True,
                                               label='Is extended')
    is_featured = django_filters.BooleanFilter(name='bird__bird_extended__is_featured',
                                               label='Is featured')

    class Meta:
        model = BandCombo
        fields = ('style', 'study_area', 'bird__status',)

class BandComboViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BandComboSerializer
    search_fields = ('name', 'bird__name',)
    ordering_fields = ('name', 'style', 'date_deployed' 'study_area',
                       'bird__name', 'bird__status', 'bird__bird_extended',)
    filter_class = BandComboFilter

    def get_queryset(self):
        queryset = BandCombo.objects. \
                   select_related('bird', 'study_area'). \
                   all()

        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset
