from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter

from birds.views import BirdViewSet
from sightings.views import SightingViewSet
from locations.views import PrimaryLocationViewSet, SecondaryLocationViewSet


router = DefaultRouter()
router.register(r'birds', BirdViewSet)
router.register(r'sightings', SightingViewSet)
router.register(r'primary_locations', PrimaryLocationViewSet)
router.register(r'secondary_locations', SecondaryLocationViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
]
