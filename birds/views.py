from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from rest_framework import viewsets

from .models import Bird
from .serializers import BirdSerializer


class BirdListView(ListView):
    model = Bird


class BirdDetailView(DetailView):
    model = Bird


class BirdViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Bird.objects.all()
    serializer_class = BirdSerializer
