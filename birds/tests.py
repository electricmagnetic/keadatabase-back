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


    def test_unique(self):
        """ Models should be unique (on id_band field) """
        with self.assertRaises(ValidationError):
            bird_original = Bird(id_band='v-12345')
            bird_duplicate = Bird(id_band='v-12345')

            bird_original.full_clean()
            bird_original.save()

            bird_duplicate.full_clean()
            bird_duplicate.save()


    def test_validate_child_secondary_location(self):
        """ Check that a secondary_location can only be added if it is a child of the
            primary_location, and that it is always paired with a primary_location """

        primary = PrimaryLocation.objects.create(name='Craigieburn Forest Park')
        secondary = SecondaryLocation.objects.create(name='Broken River Ski Area',
                                                     primary_location=primary)
        alternative_primary = PrimaryLocation.objects.create(name='Nelson Lakes National Park')

        with self.assertRaises(ValidationError):
            bird_secondary_only = Bird(id_band='v-12345', secondary_location=secondary)
            bird_secondary_only.full_clean()
            bird_secondary_only.save()

        with self.assertRaises(ValidationError):
            bird_alternative_primary = Bird(id_band='v-54321', primary_location=alternative_primary,
                                            secondary_location=secondary)
            bird_alternative_primary.full_clean()
            bird_alternative_primary.save()


    def test_validate_date_caught(self):
        """ Check that date_caught can only be today or from the past """

        with self.assertRaises(ValidationError):
            date_future = date.today() + timedelta(days=1)
            bird_future = Bird(id_band='v-12345', date_caught=date_future)
            bird_future.full_clean()
            bird_future.save()


    def test_validate_regex_id_band(self):
        """ Check only id bands matching the regex '^[a-z0-9]{1,2}-[0-9]+$' can be added """
        with self.assertRaises(ValidationError):
            bird_invalid_spaces = Bird(id_band='v - 12345')
            bird_invalid_spaces.full_clean()
            bird_invalid_spaces.save()

        with self.assertRaises(ValidationError):
            bird_invalid_uppercase = Bird(id_band='V-12345')
            bird_invalid_uppercase.full_clean()
            bird_invalid_uppercase.save()

        with self.assertRaises(ValidationError):
            bird_invalid_no_dash = Bird(id_band='V12345')
            bird_invalid_no_dash.full_clean()
            bird_invalid_no_dash.save()

        with self.assertRaises(ValidationError):
            bird_invalid_no_prefix = Bird(id_band='-12345')
            bird_invalid_no_prefix.full_clean()
            bird_invalid_no_prefix.save()


class BirdMethodTests(TestCase):
    """ Tests for methods of Bird objects """
    def test_identifier_method(self):
        """ The get_identifier method should return an appropriate name """
        bird_id_only = Bird(id_band='v-12345')
        bird_id_only.full_clean()
        bird_id_only.save()
        self.assertEqual(bird_id_only.get_identifier(), 'v-12345')

        bird_with_name = Bird(id_band='v-54321', name='Colin')
        bird_with_name.full_clean()
        bird_with_name.save()
        self.assertEqual(bird_with_name.get_identifier(), 'Colin')


    def test_location_method(self):
        """ The get_location method should return an appropriate location """
        primary = PrimaryLocation.objects.create(name='Craigieburn Forest Park')
        secondary = SecondaryLocation.objects.create(name='Broken River Ski Area',
                                                     primary_location=primary)

        bird_primary = Bird(id_band='v-12345', primary_location=primary)
        self.assertEqual(bird_primary.get_location(), 'Craigieburn Forest Park')

        bird_both = Bird(id_band='v-12345', primary_location=primary,
                         secondary_location=secondary)
        self.assertEqual(bird_both.get_location(),
                         'Craigieburn Forest Park (Broken River Ski Area)')

        bird_none = Bird(id_band='v-12345')
        self.assertEqual(bird_none.get_location(), '')


    def test_get_colour_band_method(self):
        """ The get_colour_band method should return blank if no colour_band is associated """
        band = Band(band_symbol_colour='WHITE', band_symbol='*', band_colour='BLACK')

        bird_without_band = Bird(id_band='v-12345')
        self.assertEqual(bird_without_band.get_colour_band(), '')

        bird_with_band = Bird(id_band='v-12345', band=band)
        self.assertEqual(bird_with_band.get_colour_band(), 'White "*" on Black')
