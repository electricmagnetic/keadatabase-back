"""keadatabase URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

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
    url(r'^bands_autocomplete/', include('bands.urls', namespace='bands')),
    url(r'^locations_autocomplete/', include('locations.urls', namespace='locations')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', admin.site.urls),
    url(r'^about/', TemplateView.as_view(template_name='about.html'), name='about'),
    url(r'^', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
