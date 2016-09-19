from datetime import date, timedelta, datetime

from django.test import TestCase
from django.core.exceptions import ValidationError

from .models import Sighting
from locations.models import PrimaryLocation, SecondaryLocation


class SightingObjectTests(TestCase):
    """ Tests for create/edit/delete functions of Sighting objects """
    def test_blank(self):
        """ The model should not submit if all fields are left blank """
        with self.assertRaises(ValidationError):
            bird = Sighting()
            bird.full_clean()
            bird.save()


    def test_validate_date_caught(self):
        """ Check that date_caught can only be today or from the past """
        with self.assertRaises(ValidationError):
            time_now = datetime.now().time()
            date_future = date.today() + timedelta(days=1)
            sighting_future = Sighting(date_sighted=date_future, time_sighted=time_now,
                                       first_name='John', last_name='Smith',
                                       email='test@example.org')
            sighting_future.full_clean()
            sighting_future.save()


    def test_validate_child_secondary_location(self):
        """ Check that a secondary_location can only be added if it is a child of the
            primary_location, and that it is always paired with a primary_location """
        primary = PrimaryLocation.objects.create(name='Craigieburn Forest Park')
        secondary = SecondaryLocation.objects.create(name='Broken River Ski Area',
                                                     primary_location=primary)
        alternative_primary = PrimaryLocation.objects.create(name='Nelson Lakes National Park')

        time_now = datetime.now().time()
        date_now = date.today()

        with self.assertRaises(ValidationError):
            sighting_secondary_only = Sighting(date_sighted=date_now, time_sighted=time_now,
                                               first_name='John', last_name='Smith',
                                               email='test@example.org',
                                               secondary_location=secondary)
            sighting_secondary_only.full_clean()
            sighting_secondary_only.save()

        with self.assertRaises(ValidationError):
            sighting_alternative_primary = Sighting(date_sighted=date_now, time_sighted=time_now,
                                                    first_name='John', last_name='Smith',
                                                    email='test@example.org',
                                                    primary_location=alternative_primary,
                                                    secondary_location=secondary)
            sighting_alternative_primary.full_clean()
            sighting_alternative_primary.save()
