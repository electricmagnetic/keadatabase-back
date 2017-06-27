import csv
import datetime

from django.utils import timezone
from django.core import management
from django.utils.text import slugify

from locations.models import StudyArea
from birds.models import Bird
from bands.models import BandCombo

def get_StudyArea(row):
    """ Returns a StudyArea if it matches the name obtained from the row, False otherwise """

    try:
        # Checks last word  (e.g. 'Rotoiti')
        one_word_location = ' '.join(row['Transmitter ID'].split()[-1:])
        study_area = StudyArea.objects.get(slug=slugify(one_word_location))
        return study_area
    except StudyArea.DoesNotExist:
        pass

    try:
        # Checks last two words (e.g. 'Abel Tasman')
        two_word_location = ' '.join(row['Transmitter ID'].split()[-2:])
        study_area = StudyArea.objects.get(slug=slugify(two_word_location))
        return study_area
    except StudyArea.DoesNotExist:
        pass

    try:
        # Checks second-to-last word (e.g. 'Waimakariri 2')
        second_last_word_location = ' '.join(row['Transmitter ID'].split()[-2:-1])
        study_area = StudyArea.objects.get(slug=slugify(second_last_word_location))
        return study_area
    except StudyArea.DoesNotExist:
        pass

    # if not get_StudyArea(one_word_location) and \
    #    not get_StudyArea(two_word_location) and \
    #    not one_word_location == 'Decommissioned' and \
    #    not one_word_location == 'duplicate' and \
    #    not one_word_location == '2' and \
    #    not one_word_location == '3':
    #     # TODO: check the special cases

    return False

def get_Bird(row):
    """ Returns a Bird if it matches the name obtained from the row, False otherwise """
    try:
        bird = Bird.objects.get(slug=slugify(row['Kea ID']))
        return bird
    except Bird.DoesNotExist:
        return False

def is_valid_Band(row):
    """ Returns True if given row appears to be a Band, False otherwise """

    # must have valid action
    valid_actions = ['deployed', 'transferred',]
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
    if not get_Bird(row):
        raise ValueError('No Bird exists for this band:', row['Transmitter ID'])

    # Location contained within ID must match with a StudyArea
    if not get_StudyArea(row):
        raise ValueError('No StudyArea exists for this band:', row['Transmitter ID'])

    return True

    # TODO: (verify where there is band but no bird, and bird but no band)

def standardise_BandCombo(row):
    """ Takes a given row and returns a standardised object """

    band_combo = []
    classification = classify_Band(row)
    bird = get_Bird(name)

    # determine what is noise and what is not
    # split out area and band id
    # categorise based on 'new' style or 'old' style
    # write tests
    # special characters (e.g. divides)
    # decommissioned bands
    # deploy – check date deployed, use most recent one

    return band_combo

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

            #band_combo = standardise_BandCombo(row)

            # Get associated objects
            bird = get_Bird(row)
            study_area = get_StudyArea(row)

            # Map fields
            band_combo_map = {
                'bird': bird,
                'name': row['Transmitter ID'],
                'study_area': study_area,
                'date_deployed': datetime.datetime.strptime(row['Date'], "%Y-%m-%d %H:%M:%S")
            }

            try:
                band_combo = BandCombo.objects.get(bird=bird)

                # Only updated if database-stored action is older
                if band_combo.date_deployed > band_combo_map['date_deployed'].date():
                    continue

                # TODO: only update 'modified date' if something changed

                for key, value in band_combo_map.items():
                    setattr(band_combo, key, value)
                band_combo.full_clean()
                band_combo.save()
                checked_count += 1
            except BandCombo.DoesNotExist:
                band_combo_map['date_imported'] = timezone.now()
                band_combo = BandCombo(**band_combo_map)
                band_combo.full_clean()
                band_combo.save()
                created_count += 1


    if hasattr(self, 'stdout'):
        self.stdout.write("\tChecked: %d" % checked_count)
        self.stdout.write("\tCreated: %d" % created_count)
