import csv
import datetime

from django.utils import timezone
from django.core import management
from django.utils.text import slugify

def is_valid_Band(row):
    if row['Status'] == 'Active':
        return True

    return False

def classify_Band(row):
    """ Returns type of Band, if Band - filters noise in original dataset """

    # Check whether band is either colour or letter combo
    if row['DeviceClass'] == 'Colour combo':
        return 'colour'
    if row['DeviceClass'] == 'Letter combo':
        return 'letter'

    return False

def synchronise_Band(self, transmitters_file, bands_file):
    """ Imports Band objects from data/Transmitters.csv, data/Kea\ bands.csv """

    if hasattr(self, 'stdout'):
        self.stdout.write(self.style.MIGRATE_LABEL("Band:"))

    with open(transmitters_file, 'rt') as transmitters_csv, open(bands_file, 'rt') as bands_csv:
        transmitters_reader = csv.DictReader(transmitters_csv, delimiter=',', quotechar='"')
        bands_reader = csv.DictReader(bands_csv, delimiter=',', quotechar='"')

        created_count = 0
        checked_count = 0

        for row in transmitters_reader:
            if not is_valid_Band(row):
                continue

            band_type = classify_Band(row)

            if band_type:
                print("%s %s" % (row['TR4 tune'], row['StudyArea']))

    if hasattr(self, 'stdout'):
        self.stdout.write("\tChecked: %d" % checked_count)
        self.stdout.write("\tCreated: %d" % created_count)
