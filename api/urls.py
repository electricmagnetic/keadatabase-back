from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter

from birds.views import BirdViewSet, BirdSightingViewSet
from sightings.views import SightingViewSet
from locations.views import PrimaryLocationViewSet, SecondaryLocationViewSet
from bands.views import BandViewSet


router = DefaultRouter()
router.register(r'birds', BirdViewSet)
router.register(r'bands', BandViewSet)
router.register(r'sightings', SightingViewSet)
router.register(r'bird_sightings', BirdSightingViewSet)
router.register(r'primary_locations', PrimaryLocationViewSet)
router.register(r'secondary_locations', SecondaryLocationViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
]
