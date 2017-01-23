from django import forms

from dal import autocomplete

from .models import BandCombo


class BandComboForm(forms.ModelForm):
    """ Principle BandCombo form, allows for autocomplete """

    class Meta:
        model = BandCombo
        fields = ('__all__')

        widgets = {
            'area_location':
                autocomplete.ModelSelect2(
                    url='locations:area_location_autocomplete',
                ),
        }
