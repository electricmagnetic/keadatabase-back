import django_filters
from rest_framework import viewsets

from .models import BandCombo
from .serializers import BandComboSerializer

class BandComboFilter(django_filters.FilterSet):
    colours = django_filters.BaseInFilter(lookup_expr='contains')
    symbols = django_filters.BaseInFilter(lookup_expr='contains')

    class Meta:
        model = BandCombo
        fields = ('style', 'study_area',)

class BandComboViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BandCombo.objects. \
               select_related('bird'). \
               select_related('study_area'). \
               all()
    serializer_class = BandComboSerializer
    search_fields = ('name', 'bird__name',)
    ordering_fields = ('bird', 'name', 'style', 'date_deployed',)
    filter_class = BandComboFilter
