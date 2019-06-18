from rest_framework import renderers
from rest_framework_gis.filters import TMSTileFilter

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

    bbox_filter_field = 'polygon'
    filter_backends = (TMSTileFilter, )
    bbox_filter_include_overlapping = True

    # Disable HTML view of this for compatibility
    renderer_classes = [renderers.JSONRenderer]
