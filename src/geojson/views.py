from rest_framework import renderers

from sightings.views.sightings import SightingViewSet
from sightings.views.birds import BirdSightingViewSet
from locations.views import GridTileViewSet
from keadatabase.pagination import SightingGeoJSONPagination, GridTileGeoJSONPagination, BirdSightingGeoJSONPagination
from .serializers import SightingGeoJSONSerializer, GridTileGeoJSONSerializer, BirdSightingGeoJSONSerializer

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

class BirdSightingGeoJSONViewSet(BirdSightingViewSet):
    serializer_class = BirdSightingGeoJSONSerializer
    pagination_class = BirdSightingGeoJSONPagination

    # Disable HTML view of this for compatibility
    renderer_classes = [renderers.JSONRenderer]
