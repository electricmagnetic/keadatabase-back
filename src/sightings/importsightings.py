import csv

from django.core import management

from sightings.models.sightings import SightingsSighting
from sightings.models.birds import SightingsBird
from sightings.models.contributors import Contributor

def createContributor(row):
    contributor_map = {
        'name': row['name'],
        'email': row['email'],
    }

    contributor = Contributor(**contributor_map)
    contributor.full_clean()
    contributor.save()

    return contributor


def createSightingsSighting(row, contributor):
    sighting_map = {
        'date_sighted': row['date_sighted'],
        'time_sighted': row['time_sighted'],
        'comments': row['comments'],
        'sighting_type': row['sighting_type'],
        'point_location': ("SRID=4326;POINT (%s %s)" % (row['longitude'], row['latitude'])),
        'precision': row['precision'],
        'number': row['number'],
        'location_details': row['location_details'],
        'behaviour': row['behaviour'],
        'contributor': contributor,
    }

    sighting = SightingsSighting(**sighting_map)
    sighting.full_clean()
    sighting.save()

    return sighting


def createSightingsBird(row, sighting):
    bird_map = {
        'sighting': sighting,
        'banded': 'unknown',
    }

    bird = SightingsBird(**bird_map)
    bird.full_clean()
    bird.save()

    return bird


def import_SightingsSighting(self, sightings_csv):
    """ Imports SightingsSighting objects from data/sightings.csv """

    if hasattr(self, 'stdout'):
        self.stdout.write(self.style.MIGRATE_LABEL("SightingsSighting:"))

    sightings_reader = csv.DictReader(sightings_csv, delimiter=',', quotechar='"')

    created_count = 0

    for row in sightings_reader:
        contributor = createContributor(row)
        sighting = createSightingsSighting(row, contributor)

        created_count += 1

        # Create SightingsBird object(s) if relevant
        if sighting.sighting_type == 'sighted':
            for bird_number in range(0, sighting.number):
                # TODO enable more complexity in creating SightingBirds
                bird = createSightingsBird(row,sighting)

    if hasattr(self, 'stdout'):
        self.stdout.write("\tCreated: %d" % created_count)
