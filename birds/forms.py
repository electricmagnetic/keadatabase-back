from django import forms

from dal import autocomplete

from .models import Bird


class BirdForm(forms.ModelForm):
    """ Principle bird form, allows for autocomplete """

    class Meta:
        model = Bird
        fields = ('__all__')

        widgets = {
            'primary_location':
                autocomplete.ModelSelect2(
                    url='locations:primary_location_autocomplete',
                ),
            'secondary_location':
                autocomplete.ModelSelect2(
                    url='locations:secondary_location_autocomplete',
                    forward=['primary_location'],
                ),
            'band':
                autocomplete.ModelSelect2(
                    url='bands:band_autocomplete',
                ),
        }

    class Media:
        js = ('js/autocomplete-forward.js',)
