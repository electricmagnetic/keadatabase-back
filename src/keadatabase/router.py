""" DRF router configuration """

from rest_framework.routers import DefaultRouter

from birds.views import BirdViewSet
from bands.views import BandComboViewSet
from sightings.views.observations import ObservationViewSet
from sightings.views.birds import BirdObservationViewSet
from sightings.views.media import ObservationsMediaViewSet
from geojson.views import ObservationGeoJSONViewSet, GridTileGeoJSONViewSet, BirdObservationGeoJSONViewSet
from report.views import ReportObservationViewSet
from report.views import ReportSurveyViewSet
from surveys.views import SurveyViewSet, SurveyHourViewSet, ObserverViewSet
from locations.views import GridTileViewSet
from analysis.views import GridTileAnalysisViewSet, SurveyAnalysisViewSet

router = DefaultRouter()

router.register(r'band_combos', BandComboViewSet, 'BandCombo')

router.register(r'birds', BirdViewSet, 'Bird')

router.register(r'report/sighting', ReportObservationViewSet, 'ReportObservation')
router.register(r'report/survey', ReportSurveyViewSet, 'ReportSurveyViewSet')

router.register(r'sightings/sightings', ObservationViewSet, 'Observation')
router.register(r'sightings/birds', BirdObservationViewSet, 'BirdObservation')
router.register(r'sightings/media', ObservationsMediaViewSet, 'ObservationsMedia')

router.register(r'surveys/grid_tiles', GridTileViewSet, 'GridTile')
router.register(r'surveys/hours', SurveyHourViewSet, 'SurveyHour')
router.register(r'surveys/surveys', SurveyViewSet, 'Survey')
router.register(r'surveys/observers', ObserverViewSet, 'Observer')

router.register(r'geojson/sightings', ObservationGeoJSONViewSet, 'ObservationGeoJSON')
router.register(r'geojson/grid_tiles', GridTileGeoJSONViewSet, 'GridTileGeoJSON')
router.register(r'geojson/birds', BirdObservationGeoJSONViewSet, 'BirdObservationGeoJSON')

router.register(r'analysis/grid_tiles', GridTileAnalysisViewSet, 'GridTileAnalysis')
router.register(r'analysis/surveys', SurveyAnalysisViewSet, 'SurveyAnalysis')
