from unittest import skip

from django.test import TestCase
from django.core.exceptions import ValidationError

from birds.models import Bird
from .models import Band


class BandObjectTests(TestCase):
    """ Tests for create/edit/delete functions of Band objects """
    def test_blank(self):
        """ The model should not submit if all fields are left blank """
        with self.assertRaises(ValidationError):
            band = Band()
            band.full_clean()
            band.save()


    @skip
    def test_validate_unique_colour_band(self):
        """ Check only unique (to one primary location) colour band combinations can be added """
        self.fail('TODO')


    def test_validate_unique_id_band(self):
        """ Check only unique id bands can be added """
        with self.assertRaises(ValidationError):
            band_original = Band(id_band='v-12345')
            band_duplicate = Band(id_band='v-12345')

            band_original.full_clean()
            band_original.save()

            band_duplicate.full_clean()
            band_duplicate.save()


    def test_validate_regex_id_band(self):
        """ Check only id bands matching the regex '^[a-z0-9]{1,2}-[0-9]+$' can be added """
        with self.assertRaises(ValidationError):
            band_invalid_spaces = Band(id_band='v - 12345')
            band_invalid_spaces.full_clean()
            band_invalid_spaces.save()

        with self.assertRaises(ValidationError):
            band_invalid_uppercase = Band(id_band='V-12345')
            band_invalid_uppercase.full_clean()
            band_invalid_uppercase.save()

        with self.assertRaises(ValidationError):
            band_invalid_no_dash = Band(id_band='V12345')
            band_invalid_no_dash.full_clean()
            band_invalid_no_dash.save()

        with self.assertRaises(ValidationError):
            band_invalid_no_prefix = Band(id_band='-12345')
            band_invalid_no_prefix.full_clean()
            band_invalid_no_prefix.save()


    def test_transform_colour_band_symbol(self):
        """ Check that colour band symbols are consistently transformed """
        band_uppercase = Band(id_band='v-12345', colour_band_symbol='A', colour_band_colour='WHITE',
                              colour_band_symbol_colour='BLACK')
        band_uppercase.full_clean()
        band_uppercase.save()
        self.assertEqual(band_uppercase.colour_band_symbol, 'A')

        band_lowercase = Band(id_band='v-54321', colour_band_symbol='z', colour_band_colour='BLACK',
                              colour_band_symbol_colour='WHITE')
        band_lowercase.full_clean()
        band_lowercase.save()
        self.assertEqual(band_lowercase.colour_band_symbol, 'Z')


    def test_complete_colour_band(self):
        """ Check that only fully completed colour bands are entered (i.e. no partial bands) """
        with self.assertRaises(ValidationError):
            band_partial_colour_band = Band(id_band='v-12345', colour_band_symbol='*')
            band_partial_colour_band.full_clean()
            band_partial_colour_band.save()


class BandMethodTests(TestCase):
    """ Tests for methods of Band objects """
    def test_id_band_method(self):
        """ The get_id_band method should return an appropriately formatted ID band """
        band_unknown_leg = Band(id_band='v-12345')
        self.assertEqual(band_unknown_leg.get_id_band(), 'v-12345')

        band_known_leg = Band(id_band='v-12345', id_band_leg='R')
        self.assertEqual(band_known_leg.get_id_band(), 'v-12345 [Right]')


    def test_colour_band_method(self):
        """ The get_colour_band method should return an appropriately formatted colour band """
        band_blank_colour_band = Band(id_band='v-12345')
        self.assertEqual(band_blank_colour_band.get_colour_band(), '-')

        band_colour_band = Band(id_band='v-12345', colour_band_colour='BLACK',
                                colour_band_symbol='*', colour_band_symbol_colour='WHITE')
        self.assertEqual(band_colour_band.get_colour_band(), 'White "*" on Black')


    def test_colour_band_code_method(self):
        """ The get_colour_band_code method should return an appropriately formatted code """
        band_colour_band = Band(id_band='v-12345', colour_band_colour='BLACK',
                                colour_band_symbol='*', colour_band_symbol_colour='WHITE')
        self.assertEqual(band_colour_band.get_colour_band_code(), 'WHITE-*_BLACK')


    def test_bird_method(self):
        """ The get_bird method should return a Bird identifier or a '-' """
        band1 = Band(id_band='v-12345')
        band1.full_clean()
        band1.save()

        band2 = Band(id_band='v-54321')
        band2.full_clean()
        band2.save()

        bird_with_name = Bird(band=band1, name='Colin')
        bird_with_name.full_clean()
        bird_with_name.save()
        self.assertEqual(band1.get_bird(), 'Colin')

        bird_id_only = Bird(band=band2)
        bird_id_only.full_clean()
        bird_id_only.save()
        self.assertEqual(band2.get_bird(), 'v-54321')
