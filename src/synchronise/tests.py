from django.test import TestCase
from django.core.exceptions import ValidationError

from locations.models import StudyArea
from .locations import synchronise_StudyArea

class LocationsSynchroniseTests(TestCase):
    """ Tests for synchronisation of Location models """

    def test_initial_synchronise(self):
        """ Data provided in a CSV should get added (excl. duplicates) to db."""
        self.assertEqual(StudyArea.objects.all().count(), 0)

        synchronise_StudyArea(self, "../test_data/tStudyAreas.csv")
        self.assertEqual(StudyArea.objects.all().count(), 7)
