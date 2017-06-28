from datetime import date
from dateutil.relativedelta import relativedelta
from versatileimagefield.fields import VersatileImageField, PPOIField
from versatileimagefield.image_warmer import VersatileImageFieldWarmer

from django.db import models
from django.utils.text import slugify
from django.dispatch import receiver

from locations.models import StudyArea

SEX_CHOICES = (
    ('', 'Undetermined'),
    ('F', 'Female'),
    ('M', 'Male'),
)

STATUS_CHOICES = (
    ('', 'Unknown'),
    ('+', 'Alive'),
    ('-', 'Dead'),
)

def bird_directory_path(instance, filename):
    """ Helper function for determining upload location for BirdExtended """
    return 'birds/%s/%s' % (instance.bird.slug, filename)

class Bird(models.Model):
    """ Basic bird information, designed to be imported from Access """

    name = models.CharField(max_length=100, unique=True)
    slug = models.CharField(max_length=100, primary_key=True, editable=False)

    sex = models.CharField(max_length=1, blank=True, choices=SEX_CHOICES,
                           default='')
    status = models.CharField(max_length=1, blank=True, choices=STATUS_CHOICES,
                              default='')
    birthday = models.DateField(blank=True, null=True)

    study_area = models.ForeignKey(StudyArea, related_name='birds', blank=True, null=True)

    # Metadata
    date_modified = models.DateTimeField(auto_now=True)
    date_imported = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """ Generate slug from name """

        self.slug = slugify(self.name)
        super(Bird, self).save(*args, **kwargs)

    def get_age(self):
        """ Calculates age based on birthday """

        if self.status == '-':  # No age if bird is dead
            return None
        if self.birthday == None:  # No age if no birthday
            return None

        difference_in_years = relativedelta(date.today(), self.birthday).years
        return difference_in_years

    def get_life_stage(self):
        """ Calculates life stage based on age (integers) """

        if self.get_age() == None:
            return None

        age = self.get_age()

        if age == 0:  # Under 12 months
            return 'Fledgling'
        elif age == 1:
            return 'Juvenile'
        elif age >= 2 and age < 4:
            return 'Sub-Adult'
        elif age >= 4:
            return 'Adult'
        else:
            return None

class BirdExtended(models.Model):
    """ Extended bird information, designed to be edited on Django """
    bird = models.OneToOneField(
        Bird,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='bird_extended'
    )

    is_extended = models.BooleanField(default=True, editable=False)

    is_featured = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)
    sponsor_name = models.CharField(max_length=200, null=True, blank=True)
    sponsor_website = models.URLField(max_length=200, null=True, blank=True)

    profile_picture = VersatileImageField(upload_to=bird_directory_path,
                                          blank=True, null=True,
                                          ppoi_field='profile_picture_ppoi')
    profile_picture_ppoi = PPOIField()

    class Meta:
        ordering = ['bird']
        verbose_name = 'Extended Bird'

    def __str__(self):
        return str(self.bird)

@receiver(models.signals.post_save, sender=BirdExtended)
def warm_BirdExtended_profile_pictures(sender, instance, **kwargs):
    """Ensures Person head shots are created post-save"""
    profile_picture_warmer = VersatileImageFieldWarmer(
        instance_or_queryset=instance,
        rendition_key_set='profile_picture',
        image_attr='profile_picture'
    )
    num_created, failed_to_create = profile_picture_warmer.warm()
