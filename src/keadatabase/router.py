""" DRF router configuration """

from rest_framework.routers import DefaultRouter

from locations.views import StudyAreaViewSet, RegionViewSet, CommonLocationViewSet
from birds.views import BirdViewSet
from bands.views import BandComboViewSet
from sightings.views.sightings import SightingsNonSightingViewSet

router = DefaultRouter()

router.register(r'band_combos', BandComboViewSet, 'BandCombo')

router.register(r'birds', BirdViewSet, 'Bird')

router.register(r'locations/study_areas', StudyAreaViewSet, 'StudyArea')
router.register(r'locations/regions', RegionViewSet, 'Region')
router.register(r'locations/common_locations', CommonLocationViewSet, 'CommonLocation')

#router.register(r'report', ReportViewSet)

#router.register(r'sightings/sightings', SightingsSightingViewSet, 'SightingsSighting')
router.register(r'sightings/non_sightings', SightingsNonSightingViewSet, 'SightingsNonSighting')
#router.register(r'sightings/birds', SightingsBirdViewSet, 'SightingsBird')
