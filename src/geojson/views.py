from rest_framework import renderers

from sightings.views.observations import ObservationViewSet
from sightings.views.birds import BirdObservationViewSet
from locations.views import GridTileViewSet
from keadatabase.pagination import ObservationGeoJSONPagination, GridTileGeoJSONPagination, BirdObservationGeoJSONPagination
from .serializers import ObservationGeoJSONSerializer, GridTileGeoJSONSerializer, BirdObservationGeoJSONSerializer


class ObservationGeoJSONViewSet(ObservationViewSet):
    serializer_class = ObservationGeoJSONSerializer
    pagination_class = ObservationGeoJSONPagination

    # Disable HTML view of this for compatibility
    renderer_classes = [renderers.JSONRenderer]


class GridTileGeoJSONViewSet(GridTileViewSet):
    serializer_class = GridTileGeoJSONSerializer
    pagination_class = GridTileGeoJSONPagination

    # Disable HTML view of this for compatibility
    renderer_classes = [renderers.JSONRenderer]


class BirdObservationGeoJSONViewSet(BirdObservationViewSet):
    serializer_class = BirdObservationGeoJSONSerializer
    pagination_class = BirdObservationGeoJSONPagination

    # Disable HTML view of this for compatibility
    renderer_classes = [renderers.JSONRenderer]
