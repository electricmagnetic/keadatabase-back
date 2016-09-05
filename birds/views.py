from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Bird


class BirdListView(ListView):
    model = Bird


class BirdDetailView(DetailView):
    model = Bird
