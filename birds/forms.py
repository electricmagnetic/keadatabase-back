from django import forms

from dal import autocomplete

from .models import Bird


class BirdForm(forms.ModelForm):
    """ Principle bird form, allows for autocomplete """

    class Meta:
        model = Bird
        fields = ('__all__')

        widgets = {
            'home_location':
                autocomplete.ModelSelect2(
                    url='locations:home_location_autocomplete',
                ),
        }

    class Media:
        js = ('js/autocomplete-forward.js',)
