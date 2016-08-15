from django.conf.urls import url

from .views import PrimaryLocationAutocomplete, SecondaryLocationAutocomplete


urlpatterns = [
    url(
        r'^primary_location_autocomplete/$',
        PrimaryLocationAutocomplete.as_view(),
        name='primary_location_autocomplete',
    ),
    url(
        r'^secondary_location_autocomplete/$',
        SecondaryLocationAutocomplete.as_view(),
        name='secondary_location_autocomplete',
    ),
]
