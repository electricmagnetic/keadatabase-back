from datetime import date, timedelta

from django.test import TestCase
from django.core.exceptions import ValidationError

from .models import Bird

class BirdObjectTests(TestCase):
    """ Tests for main functions of Bird objects """

    def test_blank(self):
        """ The model should not submit if all fields are left blank """
        with self.assertRaises(ValidationError):
            bird = Bird()
            bird.full_clean()
            bird.save()

    def test_unique(self):
        """ Models should be unique (on name field) """
        with self.assertRaises(ValidationError):
            bird = Bird(name='Helen Clark')
            bird_duplicate = Bird(name='Helen Clark')

            bird.full_clean()
            bird.save()

            bird_duplicate.full_clean()
            bird_duplicate.save()

    def test_slug_generated(self):
        """ Models should auto-generate a slug on save """
        bird = Bird(name='Helen Clark')
        self.assertEqual(bird.slug, '')

        bird.full_clean()
        bird.save()
        self.assertEqual(bird.slug, 'helen-clark')

class BirdFunctionTests(TestCase):
    """ Tests for custom functions of Bird objects """

    def test_get_age(self):
        """ Function should return correct age for 600-day-old bird """
        birthday = date.today() - timedelta(days=600)
        bird = Bird(name='Helen Clark', birthday=birthday)

        bird.full_clean()
        bird.save()

        self.assertEqual(bird.get_age(), 1)

    def test_no_get_age(self):
        """ Function should return None if no birthday """
        bird = Bird(name='Helen Clark', birthday=None)

        bird.full_clean()
        bird.save()

        self.assertEqual(bird.get_age(), None)

    def test_get_life_stage(self):
        """ Function should return different stages depending on birthday """
        birthday = date.today() - timedelta(days=100)
        bird_fledgling = Bird(name='Helen Clark', birthday=birthday)

        bird_fledgling.full_clean()
        bird_fledgling.save()

        self.assertEqual(bird_fledgling.get_life_stage(), 'Fledgling')

        birthday = date.today() - timedelta(days=600)
        bird_juvenile = Bird(name='Keith Moon', birthday=birthday)

        bird_juvenile.full_clean()
        bird_juvenile.save()

        self.assertEqual(bird_juvenile.get_life_stage(), 'Juvenile')

    def test_no_get_life_stage(self):
        """ Function should return None if no birthday """
        bird = Bird(name='Helen Clark', birthday=None)

        bird.full_clean()
        bird.save()

        self.assertEqual(bird.get_life_stage(), None)
