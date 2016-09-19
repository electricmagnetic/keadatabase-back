from django import forms

from dal import autocomplete

from .models import Bird


class BirdForm(forms.ModelForm):
    """ Principle bird form, allows for autocomplete """

    class Meta:
        model = Bird
        fields = ('__all__')

        # TODO: disallow creation/editing of new locations without some sort of checking

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
        }

    class Media:
        js = ('js/autocomplete-forward.js',)
