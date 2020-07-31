from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework import mixins

from .serializers import ReportObservationSerializer
from .serializers import ReportSurveySerializer

class ReportObservationBaseViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    throttle_scope = 'report'
    permission_classes = (AllowAny,)

class ReportObservationViewSet(ReportObservationBaseViewSet):
    serializer_class = ReportObservationSerializer

class ReportSurveyViewSet(ReportObservationBaseViewSet):
    serializer_class = ReportSurveySerializer
