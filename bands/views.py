from rest_framework import viewsets

from .models import Band
from .serializers import BandSerializer


class BandViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Band.objects.all()
    serializer_class = BandSerializer
    #filter_fields = ('band_symbol_colour', 'band_symbol', 'band_colour',)
