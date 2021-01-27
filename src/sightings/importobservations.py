import csv

from django.core import management

from sightings.models.observations import Sighting
from sightings.models.birds import BirdSighting
from sightings.models.contributors import Contributor


def createContributor(row):
    contributor_map = {
        'name': row['name'],
        'email': row['email'],
        'phone': row['phone'],
    }

    contributor = Contributor(**contributor_map)
    contributor.full_clean()
    contributor.save()

    return contributor


def createObservation(row, contributor):
    observation_map = {
        'import_id': row['import_id'],
        'date_sighted': row['date_sighted'],
        'time_sighted': row['time_sighted'],
        'comments': row['comments'],
        'sighting_type': row['sighting_type'],
        'point_location':
            ("SRID=4326;POINT (%s %s)" % (row['longitude'], row['latitude'])),
        'precision': row['precision'],
        'number': row['number'],
        'location_details': row['location_details'],
        'behaviour': row['behaviour'],
        'contributor': contributor,
    }

    observation = Sighting(**observation_map)
    observation.full_clean()
    observation.save()

    return observation


def createBirdObservation(row, observation):
    bird_map = {
        'sighting': observation,
        'banded': 'unknown',
    }

    bird = BirdSighting(**bird_map)
    bird.full_clean()
    bird.save()

    return bird


def import_Observation(self, observations_csv):
    """ Imports Sighting objects from data/observations.csv """

    if hasattr(self, 'stdout'):
        self.stdout.write(self.style.MIGRATE_LABEL("Observation:"))

    observations_reader = csv.DictReader(
        observations_csv, delimiter=',', quotechar='"'
    )

    created_count = 0

    for row in observations_reader:
        contributor = createContributor(row)
        observation = createObservation(row, contributor)

        created_count += 1

        # Create BirdSighting object(s) if relevant
        if observation.sighting_type == 'sighted':
            for bird_number in range(0, observation.number):
                # TODO enable more complexity in creating SightingBirds
                bird = createBirdObservation(row, observation)

    if hasattr(self, 'stdout'):
        self.stdout.write("\tCreated: %d" % created_count)
