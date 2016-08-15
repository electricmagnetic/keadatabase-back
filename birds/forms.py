from django import forms

from dal import autocomplete

from .models import Bird


class BirdForm(forms.ModelForm):
    class Meta:
        model = Bird
        fields = ('__all__')
        
        # TODO
        # (1) clear secondary location if primary location changed (
        # (2) disallow creation/editing of new locations without some sort of checking

        widgets = {
            'primary_location':
                autocomplete.ModelSelect2(
                    url='primary_location_autocomplete',
                ),
            'secondary_location':
                autocomplete.ModelSelect2(
                    url='secondary_location_autocomplete',
                    forward=['primary_location'],
                ),
        }
