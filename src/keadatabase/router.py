""" DRF router configuration """

from rest_framework.routers import DefaultRouter

from birds.views import BirdViewSet
from bands.views import BandComboViewSet
from sightings.views.sightings import SightingViewSet, NonSightingViewSet
from sightings.views.birds import SightingsBirdViewSet
from sightings.views.media import SightingsMediaViewSet
from report.views import ReportSightingViewSet, ReportNonSightingViewSet

router = DefaultRouter()

router.register(r'band_combos', BandComboViewSet, 'BandCombo')

router.register(r'birds', BirdViewSet, 'Bird')

router.register(r'report/sighting', ReportSightingViewSet, 'ReportSighting')
router.register(r'report/non_sighting', ReportNonSightingViewSet, 'ReportNonSighting')

router.register(r'sightings/sightings', SightingViewSet, 'Sighting')
router.register(r'sightings/non_sightings', NonSightingViewSet, 'NonSighting')
router.register(r'sightings/birds', SightingsBirdViewSet, 'SightingsBird')
router.register(r'sightings/media', SightingsMediaViewSet, 'SightingsMedia')
