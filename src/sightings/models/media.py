""" Media models for Sightings (sightings and non-sightings in .sightings)"""

from django.db import models
from django.dispatch import receiver

from versatileimagefield.fields import VersatileImageField, PPOIField
from versatileimagefield.image_warmer import VersatileImageFieldWarmer

from sightings.models.sightings import Sighting
from birds.models import Bird

def sighting_directory_path(instance, filename):
    """ Helper function for determining upload location for each sighting """
    return 'sighting/%s/%s' % (instance.sighting.id, filename)

class SightingsMedia(models.Model):
    """ User uploaded media for a sighting """
    sighting = models.ForeignKey(Sighting, related_name='media', on_delete=models.CASCADE)

    sighting_image = VersatileImageField(upload_to=sighting_directory_path,
                                         ppoi_field='sighting_image_ppoi')
    sighting_image_ppoi = PPOIField()

    birds = models.ManyToManyField(Bird, verbose_name="Birds in image",
                                   blank=True)

    # Optional
    caption = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'media'
        verbose_name_plural = 'media'
        ordering = ['id']

    def __str__(self):
        return "%s [%s]" % (self.id, self.sighting)

@receiver(models.signals.post_save, sender=SightingsMedia)
def warm_SightingsMedia_images(sender, instance, **kwargs):
    """Ensures SightingsMedia thumbnails are created post-save"""
    sighting_image_warmer = VersatileImageFieldWarmer(
        instance_or_queryset=instance,
        rendition_key_set='sighting_image',
        image_attr='sighting_image'
    )
    num_created, failed_to_create = sighting_image_warmer.warm()
