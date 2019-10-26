from rest_framework import viewsets

from locations.models import GridTile
from .serializers import GridTileAnalysisSerializer

class GridTileAnalysisViewSet(viewsets.ReadOnlyModelViewSet):
    """ Obtain all grid tiles with at least one survey hour """
    queryset = GridTile.objects. \
        prefetch_related('hours'). \
        exclude(hours__isnull=True)
    serializer_class = GridTileAnalysisSerializer
