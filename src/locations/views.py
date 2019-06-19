import django_filters
from rest_framework import viewsets

from keadatabase.pagination import GridTilePagination
from .serializers import GridTileSerializer
from .models import GridTile

class GridTileFilter(django_filters.FilterSet):
    has_hours = django_filters.BooleanFilter(field_name='hours',
                                            lookup_expr='isnull',
                                            exclude=True,
                                            label='Has hours')

    class Meta:
        model = GridTile
        fields = ('has_hours',)


class GridTileViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GridTileSerializer
    filter_class = GridTileFilter
    pagination_class = GridTilePagination

    def get_queryset(self):
        queryset = GridTile.objects. \
                   prefetch_related('hours'). \
                   all()

        return queryset
