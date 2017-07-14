""" DRF router configuration """

from rest_framework.routers import DefaultRouter

from locations.views import StudyAreaViewSet, RegionViewSet, CommonLocationViewSet
from birds.views import BirdViewSet
from bands.views import BandComboViewSet
from sightings.views.sightings import SightingsSightingViewSet, SightingsNonSightingViewSet
from sightings.views.birds import SightingsBirdViewSet
#from sightings.views.media import SightingsMediaViewSet
from report.views import ReportSightingViewSet, ReportNonSightingViewSet

router = DefaultRouter()

router.register(r'band_combos', BandComboViewSet, 'BandCombo')

router.register(r'birds', BirdViewSet, 'Bird')

router.register(r'locations/study_areas', StudyAreaViewSet, 'StudyArea')
router.register(r'locations/regions', RegionViewSet, 'Region')
router.register(r'locations/common_locations', CommonLocationViewSet, 'CommonLocation')

router.register(r'report/sighting', ReportSightingViewSet, 'ReportSighting')
router.register(r'report/non_sighting', ReportNonSightingViewSet, 'ReportNonSighting')

router.register(r'sightings/sightings', SightingsSightingViewSet, 'SightingsSighting')
router.register(r'sightings/non_sightings', SightingsNonSightingViewSet, 'SightingsNonSighting')
router.register(r'sightings/birds', SightingsBirdViewSet, 'SightingsBird')
#router.register(r'sightings/media', SightingsMediaViewSet, 'SightingsMedia')
