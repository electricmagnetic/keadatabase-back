from django import forms

from dal import autocomplete

from .models import Band


class BandForm(forms.ModelForm):
    """ Principle band form, allows for autocomplete """

    class Meta:
        model = Band
        fields = ('__all__')

        widgets = {
            'primary_location':
                autocomplete.ModelSelect2(
                    url='locations:primary_location_autocomplete',
                ),
        }
