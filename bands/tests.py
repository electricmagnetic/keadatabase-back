from unittest import skip

from django.test import TestCase
from django.core.exceptions import ValidationError

from birds.models import Bird
from .models import Band


class BandObjectTests(TestCase):
    """ Tests for create/edit/delete functions of Band objects """
    @skip
    def test_unique(self):
        """ Check only unique bands combinations can be added """
        with self.assertRaises(ValidationError):
            band_original = Band(style='P', identifier='', colour='BLACK', leg='L', position='S',
                                 symbol_colour='WHITE', symbol='X', size='LG')
            band_duplicate = Band(style='P', identifier='', colour='BLACK', leg='L', position='S',
                                  symbol_colour='WHITE', symbol='X', size='LG')

            band_original.full_clean()
            band_original.save()

            band_duplicate.full_clean()
            band_duplicate.save()


    @skip
    def test_complete_colour_band(self):
        """ Check that only fully completed colour bands are entered (i.e. no partial bands) """
        with self.assertRaises(ValidationError):
            band_partial_colour_band = Band(band_symbol_colour='WHITE', band_colour='BLACK')
            band_partial_colour_band.full_clean()
            band_partial_colour_band.save()


class BandMethodTests(TestCase):
    """ Tests for methods of Band objects """
    @skip
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


    @skip
    def test_band_type_method(self):
        self.fail('TODO')


    @skip
    def test_band_type_display_method(self):
        self.fail('TODO')


    @skip
    def test_band_combo_display_method(self):
        self.fail('TODO')


    @skip
    def test_str_method(self):
        """ The get_colour_band method should return an appropriately formatted colour band """
        band_colour_band = Band(band_colour='BLACK', band_symbol='*', band_symbol_colour='WHITE')
        self.assertEqual(band_colour_band.get_colour_band(), 'White "*" on Black')
