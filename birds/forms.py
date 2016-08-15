from django import forms

from dal import autocomplete

from .models import Bird


class BirdForm(forms.ModelForm):
    class Meta:
        model = Bird
        fields = ('__all__')
        widgets = {
            'primary_location': autocomplete.ModelSelect2(url='primary_location_autocomplete'),
            'secondary_location': autocomplete.ModelSelect2(url='secondary_location_autocomplete'),
        }
