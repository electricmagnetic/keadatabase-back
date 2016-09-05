from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Sighting


class SightingListView(ListView):
    model = Sighting


class SightingDetailView(DetailView):
    model = Sighting
