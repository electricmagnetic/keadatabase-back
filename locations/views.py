from dal import autocomplete

from .models import PrimaryLocation, SecondaryLocation


class PrimaryLocationAutocomplete(autocomplete.Select2QuerySetView):
    """ Provides a list of primary locations as an autocomplete """

    def get_queryset(self):
        qs = PrimaryLocation.objects.all().order_by('name')

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class SecondaryLocationAutocomplete(autocomplete.Select2QuerySetView):
    """ Provides a list of secondary locations as an autocomplete, filterable by choice of primary
        location """

    def get_queryset(self):
        qs = SecondaryLocation.objects.all().order_by('name')

        primary_location = self.forwarded.get('primary_location', None)

        if primary_location:
            qs = qs.filter(primary_location=primary_location)

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs
