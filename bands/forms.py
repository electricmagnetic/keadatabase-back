from django import forms

from dal import autocomplete

from .models import Band


class BandForm(forms.ModelForm):
    """ Principle band form, allows for autocomplete """

    class Meta:
        model = Band
        fields = ('__all__')

        # TODO: disallow creation/editing of new locations without some sort of checking

        widgets = {
            'primary_location':
                autocomplete.ModelSelect2(
                    url='locations:primary_location_autocomplete',
                ),
        }
