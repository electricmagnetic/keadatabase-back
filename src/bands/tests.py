from datetime import date, timedelta

from django.test import TestCase
from django.core.exceptions import ValidationError

from birds.models import Bird
from .models import BandCombo

class BandComboObjectTests(TestCase):
    """ Tests for main functions of BandCombo objects """

    def test_blank(self):
        """ The model should not submit if all fields are left blank """
        with self.assertRaises(ValidationError):
            band = BandCombo()
            band.full_clean()
            band.save()

    def test_bird(self):
        """ Models should require a Bird object """
        with self.assertRaises(ValidationError):
            band = BandCombo(name="Black 'C' on Yellow Otira")

            band.full_clean()
            band.save()

    def test_unique(self):
        """ Models should be unique (on name field) """
        bird = Bird(name='Helen Clark')

        with self.assertRaises(ValidationError):
            band = BandCombo(name="White 'C' on Red Otira", bird=bird)
            band_duplicate = BandCombo(name="White 'C' on Red Otira", bird=bird)

            band.full_clean()
            band.save()

            band_duplicate.full_clean()
            band_duplicate.save()
