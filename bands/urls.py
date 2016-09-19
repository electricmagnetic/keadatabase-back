from django.conf.urls import url

from .views import BandAutocomplete


urlpatterns = [
    url(
        r'^band_autocomplete/$',
        BandAutocomplete.as_view(),
        name='band_autocomplete',
    ),
]
