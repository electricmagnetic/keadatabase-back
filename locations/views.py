from dal import autocomplete

from .models import PrimaryLocation, SecondaryLocation


class PrimaryLocationAutocomplete(autocomplete.Select2QuerySetView):
    """ Provides a list of primary locations as an autocomplete """

    def get_queryset(self):
        queryset = PrimaryLocation.objects.all()

        return queryset


class SecondaryLocationAutocomplete(autocomplete.Select2QuerySetView):
    """ Provides a list of secondary locations as an autocomplete """

    def get_queryset(self):
        queryset = SecondaryLocation.objects.all()

        return queryset
