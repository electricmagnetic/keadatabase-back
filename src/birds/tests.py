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
