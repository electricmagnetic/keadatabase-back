from unittest import skip

from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

from .models import Bird
from locations.models import PrimaryLocation, SecondaryLocation


class BirdObjectTests(TestCase):
    """ Tests for create/edit/delete functions of Bird objects """

    def test_blank(self):
        """ The model should not submit if all fields are left blank """
        with self.assertRaises(IntegrityError):
            Bird.objects.create()


    def test_blank_id_band(self):
        """ The model should not submit if the compulsory id_band field is blank """
        bird = Bird(transmitter=False)

        with self.assertRaises(ValidationError):
            bird.save()
            bird.full_clean()


    @skip
    def test_validate_unique_colour_band(self):
        """ Check only unique colour band combinations can be added (in one location?) """
        self.fail('TODO')


    @skip
    def test_validate_unique_id_band(self):
        """ Check only unique id bands can be added (in one location?) """
        self.fail('TODO')


    @skip
    def test_validate_child_secondary_location(self):
        """ Check that a secondary_location can only be added if it is a child of the
            primary_location """
        self.fail('TODO')


    @skip
    def test_validate_date_caught(self):
        """ Check that date_caught can only be today or from the past """
        self.fail('TODO')


    @skip
    def test_transform_id_band(self):
        """ Check that id bands are consistently transformed """
        self.fail('TODO')


    @skip
    def test_transform_colour_band_symbol(self):
        """ Check that colour band symbols are consistently transformed """
        self.fail('TODO')


    @skip
    def test_validate_caught_location(self):
        """ Check that only valid point locations are accepted """
        self.fail('TODO')


class BirdMethodTests(TestCase):
    """ Tests for methods of Bird objects """

    def test_identifier_method(self):
        """ The get_identifier method should return an appropriate name """
        bird_id_only = Bird(id_band='V-12345')
        self.assertEqual(bird_id_only.get_identifier(), 'V-12345')

        bird_with_name = Bird(id_band='V-12345', name='Colin')
        self.assertEqual(bird_with_name.get_identifier(), 'Colin')


    def test_location_method(self):
        """ The get_location method should return an appropriate location """
        primary_location = PrimaryLocation.objects.create(name='Craigieburn Forest Park')
        secondary_location = SecondaryLocation.objects.create(name='Broken River Ski Area',
                                                              primary_location=primary_location)

        bird_primary = Bird(id_band='V-12345', primary_location=primary_location)
        self.assertEqual(bird_primary.get_location(), 'Craigieburn Forest Park')

        bird_secondary = Bird(id_band='V-12345', secondary_location=secondary_location)
        self.assertEqual(bird_secondary.get_location(), 'Broken River Ski Area')

        bird_both = Bird(id_band='V-12345', primary_location=primary_location,
                         secondary_location=secondary_location)
        self.assertEqual(bird_both.get_location(),
                         'Craigieburn Forest Park (Broken River Ski Area)')

        bird_none = Bird(id_band='V-12345')
        self.assertEqual(bird_none.get_location(), '')


    def test_id_band_method(self):
        """ The get_id_band method should return an appropriately formatted ID band """
        bird_unknown_leg = Bird(id_band='V-12345')
        self.assertEqual(bird_unknown_leg.get_id_band(), 'V-12345')

        bird_known_leg = Bird(id_band='V-12345', id_band_leg='R')
        self.assertEqual(bird_known_leg.get_id_band(), 'V-12345 [Right]')


    def test_colour_band_method(self):
        """ The get_colour_band method should return an appropriately formatted colour band """
        bird_blank_colour_band = Bird(id_band='V-12345')
        self.assertEqual(bird_blank_colour_band.get_colour_band(), '')

        bird_colour_band = Bird(id_band='V-12345', colour_band_colour='BLACK',
                                colour_band_symbol='A', colour_band_symbol_colour='WHITE')
        self.assertEqual(bird_colour_band.get_colour_band(), 'White "A" on Black')
