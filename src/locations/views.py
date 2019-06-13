from rest_framework import viewsets

from .serializers import GridTileSerializer
from .models import GridTile

class GridTileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GridTile.objects.all()
    serializer_class = GridTileSerializer
