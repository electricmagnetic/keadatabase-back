""" DRF router configuration """

from rest_framework.routers import DefaultRouter

from birds.views import BirdViewSet
from bands.views import BandComboViewSet
from sightings.views.sightings import SightingViewSet
from sightings.views.birds import BirdSightingViewSet
from sightings.views.media import SightingsMediaViewSet
from geojson.views import SightingGeoJSONViewSet, GridTileGeoJSONViewSet, BirdSightingGeoJSONViewSet
from report.views import ReportSightingViewSet
from report.views import ReportSurveyViewSet
from surveys.views import SurveyViewSet, SurveyHourViewSet, ObserverViewSet
from locations.views import GridTileViewSet
from analysis.views import GridTileAnalysisViewSet, SurveyAnalysisViewSet

router = DefaultRouter()

router.register(r'band_combos', BandComboViewSet, 'BandCombo')

router.register(r'birds', BirdViewSet, 'Bird')

router.register(r'report/sighting', ReportSightingViewSet, 'ReportSighting')
router.register(r'report/survey', ReportSurveyViewSet, 'ReportSurveyViewSet')

router.register(r'sightings/sightings', SightingViewSet, 'Sighting')
router.register(r'sightings/birds', BirdSightingViewSet, 'BirdSighting')
router.register(r'sightings/media', SightingsMediaViewSet, 'SightingsMedia')

router.register(r'surveys/grid_tiles', GridTileViewSet, 'GridTile')
router.register(r'surveys/hours', SurveyHourViewSet, 'SurveyHour')
router.register(r'surveys/surveys', SurveyViewSet, 'Survey')
router.register(r'surveys/observers', ObserverViewSet, 'Observer')

router.register(r'geojson/sightings', SightingGeoJSONViewSet, 'SightingGeoJSON')
router.register(r'geojson/grid_tiles', GridTileGeoJSONViewSet, 'GridTileGeoJSON')
router.register(r'geojson/birds', BirdSightingGeoJSONViewSet, 'BirdSightingGeoJSON')

router.register(r'analysis/grid_tiles', GridTileAnalysisViewSet, 'GridTileAnalysis')
router.register(r'analysis/surveys', SurveyAnalysisViewSet, 'SurveyAnalysis')
