import csv
import datetime

from django.utils import timezone
from django.core import management
from django.utils.text import slugify

from locations.models import StudyArea
from birds.models import Bird

def get_StudyArea(name):
    """ Returns a StudyArea if it matches the given name, False otherwise """
    try:
        study_area = StudyArea.objects.get(slug=slugify(name))
        return study_area
    except StudyArea.DoesNotExist:
        return False

def get_Bird(name):
    """ Returns a Bird if it matches the given name, False otherwise """
    try:
        bird = Bird.objects.get(slug=slugify(name))
        return bird
    except Bird.DoesNotExist:
        return False

def is_valid_Band(row):
    """ Returns True if given row appears to be a Band, False otherwise """

    # must have valid action
    valid_actions = ['deployed', 'transferred', 'decommissioned', 'off kea']
    if not row['Action'].lower() in valid_actions:
        return False

    # must not have 'kit' in ID
    if 'kit' in row['Kea ID'].lower():
        return False

    # must have valid colour
    colours = ['yellow', 'white', 'metal', 'blue', 'red', 'orange', 'silver',
               'pink', 'black', 'green', 'grey',]
    if not any(colour in row['Transmitter ID'].lower() for colour in colours):
        return False

    # must have a date
    if not row['Date']:
        return False

    # special case
    if 'yellowdot' in row['Transmitter ID']:
        return False

    # 'Kea ID' must match up with a Bird
    if not get_Bird(row['Kea ID']):
        raise ValueError('No Bird exists for this band:', row['Transmitter ID'])

    # Location contained within ID must match with a StudyArea
    one_word_location = ' '.join(row['Transmitter ID'].split()[-1:])
    two_word_location = ' '.join(row['Transmitter ID'].split()[-2:])

    if not get_StudyArea(one_word_location) and \
       not get_StudyArea(two_word_location) and \
       not one_word_location == 'Decommissioned' and \
       not one_word_location == 'duplicate' and \
       not one_word_location == '2' and \
       not one_word_location == '3':
        # TODO: remove the special cases
        print("%s | %s" % (one_word_location, two_word_location))
        raise ValueError('No StudyArea exists for this band:', row['Transmitter ID'])

    return True

    # TODO: (verify where there is band but no bird, and bird but no band)

def standardise_Band(row):
    """ Takes a given row and returns a standardised object """

    band = []
    classification = classify_Band(row)
    bird = get_Bird(name)

    # determine what is noise and what is not
    # split out area and band id
    # categorise based on 'new' style or 'old' style

    return band

def synchronise_Band(self, transmitters_file):
    """ Imports Band objects from data/Transmitter actions.csv """

    if hasattr(self, 'stdout'):
        self.stdout.write(self.style.MIGRATE_LABEL("Band:"))

    with open(transmitters_file, 'rt') as transmitters_csv:
        transmitters_reader = csv.DictReader(transmitters_csv, delimiter=',', quotechar='"')

        created_count = 0
        checked_count = 0

        for row in transmitters_reader:
            if not is_valid_Band(row):
                continue

            #band = standardise_Band(row)

            print('"%s" %s to %s on %s' % (row['Transmitter ID'], row['Action'].lower(), row['Kea ID'], row['Date']))


    if hasattr(self, 'stdout'):
        self.stdout.write("\tChecked: %d" % checked_count)
        self.stdout.write("\tCreated: %d" % created_count)
