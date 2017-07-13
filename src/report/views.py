from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework import mixins

from .serializers import ReportSightingSerializer, ReportNonSightingSerializer

class ReportSightingBaseViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = (AllowAny,)

class ReportSightingViewSet(ReportSightingBaseViewSet):
    serializer_class = ReportSightingSerializer

class ReportNonSightingViewSet(ReportSightingBaseViewSet):
    serializer_class = ReportNonSightingSerializer
