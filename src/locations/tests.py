from django.test import TestCase
from django.core.exceptions import ValidationError

from .models import StudyArea

class StudyAreaObjectTests(TestCase):
    """ Tests for main functions of StudyArea objects """
    def test_blank(self):
        """ The model should not submit if all fields are left blank """
        with self.assertRaises(ValidationError):
            study_area = StudyArea()
            study_area.full_clean()
            study_area.save()


    def test_unique(self):
        """ Models should be unique (on name field) """
        with self.assertRaises(ValidationError):
            study_area = StudyArea(name='Christchurch')
            study_area_duplicate = StudyArea(name='Christchurch')

            study_area.full_clean()
            study_area.save()

            study_area_duplicate.full_clean()
            study_area_duplicate.save()

    def test_unique(self):
        """ Models should be unique (on name field) """
        with self.assertRaises(ValidationError):
            study_area = StudyArea(name='Christchurch')
            study_area_duplicate = StudyArea(name='Christchurch')

            study_area.full_clean()
            study_area.save()

            study_area_duplicate.full_clean()
            study_area_duplicate.save()

    def test_slug_generated(self):
        """ Models should auto-generate a slug on save """

        study_area = StudyArea(name='Christchurch')
        self.assertEqual(study_area.slug, '')

        study_area.full_clean()
        study_area.save()
        self.assertEqual(study_area.slug, 'christchurch')
