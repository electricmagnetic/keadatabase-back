from rest_framework import serializers
from versatileimagefield.serializers import VersatileImageFieldSerializer

from ..models.media import SightingsMedia

class ObservationsMediaSerializer(serializers.ModelSerializer):
    sighting_image = VersatileImageFieldSerializer(
        sizes='sighting_image'
    )

    class Meta:
        model = SightingsMedia
        exclude = ('sighting_image_ppoi',)
