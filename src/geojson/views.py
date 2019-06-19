from rest_framework import renderers

from sightings.views.sightings import SightingViewSet
from locations.views import GridTileViewSet
from keadatabase.pagination import SightingGeoJSONPagination, GridTileGeoJSONPagination
from .serializers import SightingGeoJSONSerializer, GridTileGeoJSONSerializer

class SightingGeoJSONViewSet(SightingViewSet):
    serializer_class = SightingGeoJSONSerializer
    pagination_class = SightingGeoJSONPagination

    # Disable HTML view of this for compatibility
    renderer_classes = [renderers.JSONRenderer]

class GridTileGeoJSONViewSet(GridTileViewSet):
    serializer_class = GridTileGeoJSONSerializer
    pagination_class = GridTileGeoJSONPagination

    # Disable HTML view of this for compatibility
    renderer_classes = [renderers.JSONRenderer]
