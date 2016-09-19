from rest_framework import viewsets

from .models import Band
from .serializers import BandSerializer


class BandViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Band.objects.all()
    serializer_class = BandSerializer
