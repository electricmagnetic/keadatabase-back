from dal import autocomplete
from rest_framework import viewsets

from .models import Band
from .serializers import BandSerializer


class BandAutocomplete(autocomplete.Select2QuerySetView):
    """ Provides a list of bands as an autocomplete """

    def get_queryset(self):
        qs = Band.objects.all()

        # TODO: Refer to issue #2
        #if self.q:
            #qs = qs.filter(id_band__istartswith=self.q)

        return qs


class BandViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Band.objects.all()
    serializer_class = BandSerializer
    #filter_fields = ('band_symbol_colour', 'band_symbol', 'band_colour',)
