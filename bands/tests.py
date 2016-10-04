from unittest import skip

from django.test import TestCase
from django.core.exceptions import ValidationError

from birds.models import Bird
from locations.models import PrimaryLocation
from .models import Band


class BandObjectTests(TestCase):
    """ Tests for create/edit/delete functions of Band objects """
    def test_blank(self):
        """ The model should not submit if all fields are left blank """
        with self.assertRaises(ValidationError):
            band = Band()
            band.full_clean()
            band.save()


    def test_unique(self):
        """ Check only unique (to one primary location) colour band combinations can be added """
        with self.assertRaises(ValidationError):
            primary_location = PrimaryLocation.objects.create(name='Craigieburn Forest Park')

            band_original = Band(band_symbol_colour='WHITE', band_symbol='X', band_colour='BLACK',
                                 primary_location=primary_location)
            band_duplicate = Band(band_symbol_colour='WHITE', band_symbol='X', band_colour='BLACK',
                                  primary_location=primary_location)

            band_original.full_clean()
            band_original.save()

            band_duplicate.full_clean()
            band_duplicate.save()


    def test_transform_band_symbol(self):
        """ Check that colour band symbols are consistently transformed """
        band_uppercase = Band(band_symbol_colour='WHITE', band_symbol='X', band_colour='BLACK')
        band_uppercase.full_clean()
        band_uppercase.save()
        self.assertEqual(band_uppercase.band_symbol, 'X')

        band_lowercase = Band(band_symbol_colour='WHITE', band_symbol='z', band_colour='BLACK')
        band_lowercase.full_clean()
        band_lowercase.save()
        self.assertEqual(band_lowercase.band_symbol, 'Z')


    def test_complete_colour_band(self):
        """ Check that only fully completed colour bands are entered (i.e. no partial bands) """
        with self.assertRaises(ValidationError):
            band_partial_colour_band = Band(band_symbol_colour='WHITE', band_colour='BLACK')
            band_partial_colour_band.full_clean()
            band_partial_colour_band.save()


class BandMethodTests(TestCase):
    """ Tests for methods of Band objects """
    def test_colour_band_method(self):
        """ The get_colour_band method should return an appropriately formatted colour band """
        band_colour_band = Band(band_colour='BLACK', band_symbol='*', band_symbol_colour='WHITE')
        self.assertEqual(band_colour_band.get_colour_band(), 'White "*" on Black')


    def test_colour_band_code_method(self):
        """ The get_colour_band_code method should return an appropriately formatted code """
        band_colour_band = Band(band_colour='BLACK', band_symbol='*', band_symbol_colour='WHITE')
        self.assertEqual(band_colour_band.get_colour_band_code(), 'WHITE-*_BLACK')


    def test_bird_method(self):
        """ The get_bird method should return a Bird identifier or a '-' """
        band1 = Band(band_symbol_colour='WHITE', band_symbol='X', band_colour='BLACK')
        band1.full_clean()
        band1.save()

        band2 = Band(band_symbol_colour='WHITE', band_symbol='Z', band_colour='BLACK')
        band2.full_clean()
        band2.save()

        bird_with_name = Bird(band=band1, name='Colin', id_band='v-12345')
        bird_with_name.full_clean()
        bird_with_name.save()
        self.assertEqual(band1.get_bird(), 'Colin')

        bird_id_only = Bird(band=band2, id_band='v-54321')
        bird_id_only.full_clean()
        bird_id_only.save()
        self.assertEqual(band2.get_bird(), 'v-54321')
