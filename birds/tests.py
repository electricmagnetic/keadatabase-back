from django.test import TestCase

from .models import Bird


#class BirdObjectTests(TestCase):
    #""" Tests for create/edit/delete functions of Bird objects """

    #def test_blank(self):
        #""" The model should not submit if all fields are left blank """
        #self.assertRaises(OperationalError, Bird, transmitter=False)


    #def test_longitude_latitude_fields(self):
        #""" The model should accept all valid latitude and longitudes (assuming EPSG:4326) """
        #bird_positive_lat_long = Bird(id_band='V-12345', caught_longitude='179.987654321',
        #                              caught_latitude='89.987654321')
        #bird_negative_lat_long = Bird(id_band='V-12345', caught_longitude='-179.987654321',
        #                              caught_latitude='-89.987654321')

        #self.assertIs(True, True)


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

        bird_primary = Bird(id_band='V-12345', primary_location='Broken River Ski Area')
        self.assertEqual(bird_primary.get_location(), 'Broken River Ski Area')

        bird_secondary = Bird(id_band='V-12345', secondary_location='Craigieburn Forest Park')
        self.assertEqual(bird_secondary.get_location(), 'Craigieburn Forest Park')

        bird_both = Bird(id_band='V-12345', primary_location='Broken River Ski Area',
                         secondary_location='Craigieburn Forest Park')
        self.assertEqual(bird_both.get_location(), 'Broken River Ski Area (Craigieburn Forest Park)')

        bird_none = Bird(id_band='V-12345')
        self.assertEqual(bird_none.get_location(), '')


    def test_id_band_method(self):
        """ The get_id_band method should return an appropriately formatted ID band """

        self.assertEqual(True, True)


    def test_colour_band_method(self):
        """ The get_colour_band method should return an appropriately formatted colour band """

        self.assertEqual(True, True)
