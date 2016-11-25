from django.test import TestCase
from django.core.exceptions import ValidationError

from birds.models import Bird
from .models import Band, BandCombo


class BandComboObjectTests(TestCase):
    """ Tests for create/edit/delete functions of BandCombo objects """
    def test_blank(self):
        """ The model should not submit if all fields are left blank """
        with self.assertRaises(ValidationError):
            band_combo = BandCombo()
            band_combo.full_clean()
            band_combo.save()


class BandComboMethodTests(TestCase):
    """ Tests for methods of BandCombo objects """
    def test_str(self):
        """ Checks that BandCombos are appropriately formatted depending on type """
        self.fail('TODO')


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


    def test_validation_band_combo_type(self):
        """ Check that validation of band_type against parent band_combo type works"""
        band_combo_n = BandCombo(combo_type='N')
        band_combo_n.full_clean()
        band_combo_n.save()

        band_new = Band(band_combo=band_combo_n, style='P', identifier='', size='',
                        colour='YELLOW', position='', leg='', symbol_colour='BLACK',
                        symbol='X',)
        band_new.full_clean()
        band_new.save()

        band_identifier = Band(band_combo=band_combo_n, style='M', identifier='v-12345',
                               size='', colour='UNCOLOURED', position='', leg='',
                               symbol_colour='', symbol='',)
        band_identifier.full_clean()
        band_identifier.save()

        with self.assertRaises(ValidationError):
            band_old = Band(band_combo=band_combo_n, style='M', identifier='v-12345', size='',
                            colour='BLUE', position='T', leg='L', symbol_colour='', symbol='',)
            band_old.full_clean()
            band_old.save()


    def test_validation_single_primary(self):
        """ Check that validation of single primary Band per BandCombo works """
        ## > 1 primary Band objects (greater than)
        band_combo_gt = BandCombo()
        band_combo_gt.full_clean()
        band_combo_gt.save()

        band_primary1 = Band(band_combo=band_combo_gt, primary=True, style='M',
                             identifier='v-12345', size='', colour='UNCOLOURED', position='',
                             leg='', symbol_colour='', symbol='',)
        band_primary1.full_clean()
        band_primary1.save()

        with self.assertRaises(ValidationError):
            band_primary2 = Band(band_combo=band_combo_gt, primary=True, style='M',
                                 identifier='v-54321', size='', colour='UNCOLOURED', position='',
                                 leg='', symbol_colour='', symbol='',)
            band_primary2.full_clean()
            band_primary2.save()

        ## < 1 primary Band objects (less than)
        with self.assertRaises(ValidationError):
            band_combo_lt = BandCombo()
            band_combo_lt.full_clean()
            band_combo_lt.save()

            band_no_primary = Band(band_combo=band_combo_lt, style='P', identifier='', size='',
                                   colour='YELLOW', position='', leg='', symbol_colour='BLACK',
                                   symbol='X',)
            band_no_primary.full_clean()
            band_no_primary.save()


    def test_band_type_update(self):
        """ Check that the band_type field is updated on save """
        band = Band(style='P', identifier='', size='', colour='YELLOW', position='', leg='',
                    symbol_colour='BLACK', symbol='X',)
        band.full_clean()
        band.save()
        self.assertEqual(band.get_band_type(), band.band_type)


class BandMethodTests(TestCase):
    """ Tests for methods of Band objects """
    def test_get_bird_display(self):
        """ Checks that a Bird is returned if the Band is associated with an assigned BandCombo """
        band_bird_combo = BandCombo()
        bird = Bird(band_combo=band_bird_combo)
        band_bird = Band(band_combo=band_bird_combo, style='M', identifier='v-12345', size='',
                         colour='UNCOLOURED', position='', leg='', symbol_colour='', symbol='',)
        self.assertEqual(band_bird.get_bird_display(), bird.__str__())

        band_no_bird_combo = BandCombo()
        band_no_bird = Band(band_combo=band_no_bird_combo, style='M', identifier='v-12345', size='',
                            colour='UNCOLOURED', position='', leg='', symbol_colour='', symbol='',)
        self.assertEqual(band_no_bird.get_bird_display(), '-')


    def get_combo_display(self):
        """ Check that the appropriate combo string is returned based on the band_type """
        band_new = Band(style='P', identifier='', size='', colour='YELLOW',
                        position='', leg='', symbol_colour='BLACK', symbol='X',)
        band_new.full_clean()
        band_new.save()
        self.assertEqual(band_new.get_combo_display(), 'Black "X" on Yellow')

        band_old = Band(style='M', identifier='v-12345', size='', colour='BLUE',
                        position='T', leg='L', symbol_colour='', symbol='',)
        band_old.full_clean()
        band_old.save()
        self.assertEqual(band_old.get_combo_display(), 'Blue Top Left')

        band_identifier = Band(style='M', identifier='v-12345', size='', colour='UNCOLOURED',
                               position='', leg='', symbol_colour='', symbol='',)
        band_identifier.full_clean()
        band_identifier.save()
        self.assertEqual(band_identifier.get_combo_display(), '')


    def test_str(self):
        """ Checks that bands are appropriately formatted depending on type """
        band_new = Band(style='P', identifier='', size='', colour='YELLOW',
                        position='', leg='', symbol_colour='BLACK', symbol='X',)
        band_new.full_clean()
        band_new.save()
        self.assertEqual(band_new.__str__(), 'Black "X" on Yellow')

        band_old = Band(style='M', identifier='v-12345', size='', colour='BLUE',
                        position='T', leg='L', symbol_colour='', symbol='',)
        band_old.full_clean()
        band_old.save()
        self.assertEqual(band_old.__str__(), 'Blue Top Left [v-12345]')

        band_identifier = Band(style='M', identifier='v-12345', size='', colour='UNCOLOURED',
                               position='', leg='', symbol_colour='', symbol='',)
        band_identifier.full_clean()
        band_identifier.save()
        self.assertEqual(band_identifier.__str__(), '[v-12345]')
