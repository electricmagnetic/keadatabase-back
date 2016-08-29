from django.views.generic.list import ListView

from birds.models import Bird


class BirdListView(ListView):
    model = Bird
