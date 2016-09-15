from unittest import skip
from datetime import date, timedelta

from django.test import TestCase
from django.core.exceptions import ValidationError

from .models import Bird
from locations.models import PrimaryLocation, SecondaryLocation


class BirdObjectTests(TestCase):
    """ Tests for create/edit/delete functions of Bird objects """
    def test_blank(self):
        """ The model should not submit if all fields are left blank """
        with self.assertRaises(ValidationError):
            bird = Bird()
            bird.full_clean()
            bird.save()


    @skip
    def test_validate_unique_colour_band(self):
        """ Check only unique (to one primary location) colour band combinations can be added """
        self.fail('TODO')


    def test_validate_unique_id_band(self):
        """ Check only unique id bands can be added """
        with self.assertRaises(ValidationError):
            bird_original = Bird(id_band='v-12345')
            bird_duplicate = Bird(id_band='v-12345')

            bird_original.full_clean()
            bird_original.save()

            bird_duplicate.full_clean()
            bird_duplicate.save()


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


    def test_transform_colour_band_symbol(self):
        """ Check that colour band symbols are consistently transformed """
        bird_uppercase = Bird(id_band='v-12345', colour_band_symbol='A', colour_band_colour='WHITE',
                              colour_band_symbol_colour='BLACK')
        bird_uppercase.full_clean()
        bird_uppercase.save()
        self.assertEqual(bird_uppercase.colour_band_symbol, 'A')

        bird_lowercase = Bird(id_band='v-54321', colour_band_symbol='z', colour_band_colour='BLACK',
                              colour_band_symbol_colour='WHITE')
        bird_lowercase.full_clean()
        bird_lowercase.save()
        self.assertEqual(bird_lowercase.colour_band_symbol, 'Z')


    def test_complete_colour_band(self):
        """ Check that only fully completed colour bands are entered (i.e. no partial bands) """
        with self.assertRaises(ValidationError):
            bird_partial_colour_band = Bird(id_band='v-12345', colour_band_symbol='*')
            bird_partial_colour_band.full_clean()
            bird_partial_colour_band.save()


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


    def test_id_band_method(self):
        """ The get_id_band method should return an appropriately formatted ID band """
        bird_unknown_leg = Bird(id_band='v-12345')
        self.assertEqual(bird_unknown_leg.get_id_band(), 'v-12345')

        bird_known_leg = Bird(id_band='v-12345', id_band_leg='R')
        self.assertEqual(bird_known_leg.get_id_band(), 'v-12345 [Right]')


    def test_colour_band_method(self):
        """ The get_colour_band method should return an appropriately formatted colour band """
        bird_blank_colour_band = Bird(id_band='v-12345')
        self.assertEqual(bird_blank_colour_band.get_colour_band(), '')

        bird_colour_band = Bird(id_band='v-12345', colour_band_colour='BLACK',
                                colour_band_symbol='*', colour_band_symbol_colour='WHITE')
        self.assertEqual(bird_colour_band.get_colour_band(), 'White "*" on Black')


    def test_colour_band_code_method(self):
        """ The get_colour_band_code method should return an appropriately formatted code """
        bird_colour_band = Bird(id_band='v-12345', colour_band_colour='BLACK',
                                colour_band_symbol='*', colour_band_symbol_colour='WHITE')
        self.assertEqual(bird_colour_band.get_colour_band_code(), 'WHITE-*_BLACK')
