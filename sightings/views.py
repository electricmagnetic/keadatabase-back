from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from rest_framework import viewsets

from .models import Sighting
from .serializers import SightingSerializer


class SightingListView(ListView):
    model = Sighting


class SightingDetailView(DetailView):
    model = Sighting


class SightingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Sighting.objects.all()
    serializer_class = SightingSerializer
