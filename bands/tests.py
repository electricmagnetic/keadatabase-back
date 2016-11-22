from django.test import TestCase
from django.core.exceptions import ValidationError

from birds.models import Bird
from .models import Band, BandCombo


class BandObjectTests(TestCase):
    """ Tests for create/edit/delete functions of Band objects """
    def test_blank(self):
        """ The model should not submit if all fields are left blank """
        with self.assertRaises(ValidationError):
            band = Band()
            band.full_clean()
            band.save()


    def test_unique(self):
        """ Check only unique bands combinations can be added """
        with self.assertRaises(ValidationError):
            band_original = Band(style='P', identifier='', size='LG', colour='BLACK', position='S',
                                 leg='L', symbol_colour='WHITE', symbol='X',)
            band_duplicate = Band(style='P', identifier='', size='LG', colour='BLACK', position='S',
                                  leg='L', symbol_colour='WHITE', symbol='X',)

            band_original.full_clean()
            band_original.save()

            band_duplicate.full_clean()
            band_duplicate.save()


    def test_complete_letter_band(self):
        """ Check that only fully completed letter bands are entered (i.e. no partial bands) """
        with self.assertRaises(ValidationError):
            band_partial = Band(style='P', identifier='', size='LG', colour='BLACK', position='S',
                                leg='L', symbol_colour='WHITE', symbol='',)
            band_partial.full_clean()
            band_partial.save()


    def test_complete_colour_band(self):
        """ Check that only fully completed colour bands are entered (i.e. no partial bands) """
        with self.assertRaises(ValidationError):
            band_partial = Band(style='M', identifier='v-1234', size='LG', colour='BLACK',
                                position='S', leg='', symbol_colour='', symbol='',)
            band_partial.full_clean()
            band_partial.save()


    def test_complete_identifier_band(self):
        """ Check that only fully completed identifier bands are entered (i.e. no partial bands) """
        with self.assertRaises(ValidationError):
            band_partial = Band(style='M', identifier='', size='', colour='UNCOLOURED',
                                position='', leg='', symbol_colour='', symbol='',)
            band_partial.full_clean()
            band_partial.save()


    #band_combo='', primary=False, style='', identifier= '', size='', colour='', position='', leg='', symbol_colour='', symbol=''
    def test_validation_identifier(self):
        """ Check only identifiers matching the regex '^[a-z0-9]{1,2}-[0-9]+$' can be added """
        with self.assertRaises(ValidationError):
            band_spaces = Band(style='M', identifier='v - 12345', size='', colour='UNCOLOURED',
                               position='', leg='', symbol_colour='', symbol='',)
            band_spaces.full_clean()
            band_spaces.save()

        with self.assertRaises(ValidationError):
            band_uppercase = Band(style='M', identifier='V-12345', size='', colour='UNCOLOURED',
                                  position='', leg='', symbol_colour='', symbol='',)
            band_uppercase.full_clean()
            band_uppercase.save()

        with self.assertRaises(ValidationError):
            band_no_dash = Band(style='M', identifier='v12345', size='', colour='UNCOLOURED',
                                position='', leg='', symbol_colour='', symbol='',)
            band_no_dash.full_clean()
            band_no_dash.save()

        with self.assertRaises(ValidationError):
            band_no_prefix = Band(style='M', identifier='-12345', size='', colour='UNCOLOURED',
                                  position='', leg='', symbol_colour='', symbol='',)
            band_no_prefix.full_clean()
            band_no_prefix.save()


class BandMethodTests(TestCase):
    """ Tests for methods of Band objects """
    def test_get_bird_display(self):
        """ Checks that a Bird is returned if the Band is associated with an assigned BandCombo """
        band_combo = BandCombo()
        bird = Bird(band_combo=band_combo)
        band = Band(band_combo=band_combo, style='M', identifier='v-12345', size='',
                    colour='UNCOLOURED', position='', leg='', symbol_colour='', symbol='',)
        self.assertEqual(band.get_bird_display(), bird.__str__())



    def test_get_band_type_display(self):
        """ Checks that the appropiate human-readable choice is returned """
        band = Band(style='M', identifier='v-12345', size='', colour='UNCOLOURED',
                    position='', leg='', symbol_colour='', symbol='',)
        self.assertEqual(band.get_band_type_display(), 'Identifier (Metal)')


    def test_get_band_combo_display(self):
        """ Checks that the str function of the BandCombo is returned, only if assigned """
        band_combo = BandCombo()
        band_with = Band(band_combo=band_combo, style='M', identifier='v-12345', size='',
                         colour='UNCOLOURED', position='', leg='', symbol_colour='', symbol='',)
        self.assertEqual(band_with.get_band_combo_display(), band_combo.__str__())

        band_without = Band(style='M', identifier='v-12345', size='', colour='UNCOLOURED',
                            position='', leg='', symbol_colour='', symbol='',)
        self.assertEqual(band_without.get_band_combo_display(), 'Unallocated')


    def test_str(self):
        """ Checks that bands are appropriately formatted depending on type """
        band_new = Band(style='P', identifier='', size='', colour='YELLOW',
                        position='', leg='', symbol_colour='BLACK', symbol='X',)
        self.assertEqual(band_new.__str__(), 'Black "X" on Yellow')

        band_old = Band(style='M', identifier='v-12345', size='', colour='BLUE',
                        position='T', leg='L', symbol_colour='', symbol='',)
        self.assertEqual(band_old.__str__(), 'Blue Top Left [v-12345]')

        band_identifier = Band(style='M', identifier='v-12345', size='', colour='UNCOLOURED',
                               position='', leg='', symbol_colour='', symbol='',)
        self.assertEqual(band_identifier.__str__(), '[v-12345]')
