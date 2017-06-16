import csv
import datetime

from django.utils import timezone
from django.core import management
from django.utils.text import slugify

from birds.models import Bird

def is_valid_Band(row):
    """ Returns True if given row appears to be a Band, False otherwise """

    action = row['Action'].lower()
    if action == 'deployed':
        return True
    elif action == 'transferred':
        return True

    return False

def get_Bird(name):
    """ Returns a Bird object if it matches the given name, False otherwise """
    
    # check that bird for the combo exists
    # (verify where there is band but no bird, and bird but no band)

    pass

def classify_Band(row):
    """ Returns type of Band, if Band - filters noise in original dataset """

    # determine what is noise and what is not
    # split out area and band id
    # categorise based on 'new' style or 'old' style

    pass

def standardise_Band(row):
    """ Takes a given row and returns a standardised object that can be created """

    band = []
    classification = classify_Band(row)
    bird = get_Bird(name)

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

            band = standardise_Band(row)
            # add band as Django object

            #print ('"%s", "%s", "%s", "%s"' % (row['Kea ID'], row['Transmitter ID'].rsplit(None, 1)[0], row['Transmitter ID'].rsplit(None, 1)[-1], row['Date']))


    if hasattr(self, 'stdout'):
        self.stdout.write("\tChecked: %d" % checked_count)
        self.stdout.write("\tCreated: %d" % created_count)
