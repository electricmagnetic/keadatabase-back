from rest_framework import viewsets

from .models import Sighting
from .serializers import SightingSerializer


class SightingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Sighting.objects.all()
    serializer_class = SightingSerializer
