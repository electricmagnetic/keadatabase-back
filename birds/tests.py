from datetime import date, timedelta

from django.test import TestCase
from django.core.exceptions import ValidationError

from .models import Bird
from locations.models import PrimaryLocation, SecondaryLocation
from bands.models import Band


class BirdObjectTests(TestCase):
    """ Tests for create/edit/delete functions of Bird objects """
    def test_blank(self):
        """ The model should not submit if all fields are left blank """
        with self.assertRaises(ValidationError):
            bird = Bird()
            bird.full_clean()
            bird.save()


    def test_validate_child_secondary_location(self):
        """ Check that a secondary_location can only be added if it is a child of the
            primary_location, and that it is always paired with a primary_location """
        band1 = Band(id_band='v-12345')
        band2 = Band(id_band='v-54321')

        primary = PrimaryLocation.objects.create(name='Craigieburn Forest Park')
        secondary = SecondaryLocation.objects.create(name='Broken River Ski Area',
                                                     primary_location=primary)
        alternative_primary = PrimaryLocation.objects.create(name='Nelson Lakes National Park')

        with self.assertRaises(ValidationError):
            bird_secondary_only = Bird(band=band1, secondary_location=secondary)
            bird_secondary_only.full_clean()
            bird_secondary_only.save()

        with self.assertRaises(ValidationError):
            bird_alternative_primary = Bird(band=band2, primary_location=alternative_primary,
                                            secondary_location=secondary)
            bird_alternative_primary.full_clean()
            bird_alternative_primary.save()


    def test_validate_date_caught(self):
        """ Check that date_caught can only be today or from the past """
        band1 = Band(id_band='v-12345')

        with self.assertRaises(ValidationError):
            date_future = date.today() + timedelta(days=1)
            bird_future = Bird(band=band1, date_caught=date_future)
            bird_future.full_clean()
            bird_future.save()


class BirdMethodTests(TestCase):
    """ Tests for methods of Bird objects """
    def test_identifier_method(self):
        """ The get_identifier method should return an appropriate name """
        band1 = Band(id_band='v-12345')
        band1.full_clean()
        band1.save()

        band2 = Band(id_band='v-54321')
        band2.full_clean()
        band2.save()

        bird_id_only = Bird(band=band1)
        bird_id_only.full_clean()
        bird_id_only.save()
        self.assertEqual(bird_id_only.get_identifier(), 'v-12345')

        bird_with_name = Bird(band=band2, name='Colin')
        bird_with_name.full_clean()
        bird_with_name.save()
        self.assertEqual(bird_with_name.get_identifier(), 'Colin')


    def test_location_method(self):
        """ The get_location method should return an appropriate location """
        band1 = Band(id_band='v-12345')

        primary = PrimaryLocation.objects.create(name='Craigieburn Forest Park')
        secondary = SecondaryLocation.objects.create(name='Broken River Ski Area',
                                                     primary_location=primary)

        bird_primary = Bird(band=band1, primary_location=primary)
        self.assertEqual(bird_primary.get_location(), 'Craigieburn Forest Park')

        bird_both = Bird(band=band1, primary_location=primary,
                         secondary_location=secondary)
        self.assertEqual(bird_both.get_location(),
                         'Craigieburn Forest Park (Broken River Ski Area)')

        bird_none = Bird(band=band1)
        self.assertEqual(bird_none.get_location(), '')
