from rest_framework import renderers

from sightings.views.sightings import SightingViewSet
from keadatabase.pagination import SightingGeoJSONPagination
from .serializers import SightingGeoJSONSerializer

class SightingGeoJSONViewSet(SightingViewSet):
    serializer_class = SightingGeoJSONSerializer
    pagination_class = SightingGeoJSONPagination

    # Disable HTML view of this for compatibility
    renderer_classes = [renderers.JSONRenderer]
