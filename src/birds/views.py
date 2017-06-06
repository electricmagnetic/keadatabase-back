from rest_framework import viewsets

from .models import Bird
from .serializers import BirdSerializer

class BirdViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Bird.objects.all()
    serializer_class = BirdSerializer
    #filter_fields = ('name',)
