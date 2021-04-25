import csv
import datetime
import re

from django.utils import timezone
from django.utils.text import slugify

from locations.models import StudyArea
from birds.models import Bird
from bands.models import BandCombo

COLOURS = [
    'yellow',
    'white',
    'metal',
    'blue',
    'red',
    'orange',
    'silver',
    'pink',
    'black',
    'green',
    'grey',
    'lime',
    'purple',
    'brown',
    'lightblue',
]


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
        second_last_word_location = ' '.join(
            row['Transmitter ID'].split()[-2:-1]
        )
        study_area = StudyArea.objects.get(
            slug=slugify(second_last_word_location)
        )
        return study_area
    except StudyArea.DoesNotExist:
        pass

    return False


def get_Bird(row):
    """ Returns a Bird if it matches the name obtained from the row, False otherwise """
    try:
        bird = Bird.objects.get(slug=slugify(row['Kea ID']))
        return bird
    except Bird.DoesNotExist:
        return False


def is_valid_BandCombo(row):
    """ Returns True if given row appears to be a BandCombo, False otherwise """

    # must have valid action
    valid_actions = [
        'deployed',
        'transferred',
    ]
    if not row['Action'].lower() in valid_actions:
        return False

    # must not have 'kit' in ID
    if 'kit' in row['Kea ID'].lower():
        return False

    # must have valid colour
    if not any(colour in row['Transmitter ID'].lower() for colour in COLOURS):
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
        raise ValueError(
            'No StudyArea exists for this band:', row['Transmitter ID']
        )

    return True

    # TODO: (verify where there is band but no bird, and bird but no band)


def standardise_BandCombo(row, bird, study_area):
    """ Takes a given row, bird and study_area and returns a standardised object """

    standardised_bc = {
        'bird':
            bird,
        'study_area':
            study_area,
        'date_deployed':
            datetime.datetime.strptime(row['Date'], "%Y-%m-%d %H:%M:%S").date(),
    }

    raw_bc_str = row['Transmitter ID']

    # [common] remove identified StudyArea from raw string
    raw_bc_str = raw_bc_str.replace(str(study_area), "")

    # [common] determine style (new/old) - looks for 'on' as a standalone word
    if re.search(r'\bon\b', raw_bc_str.lower()) is not None:
        standardised_bc['style'] = 'new'
    else:
        standardised_bc['style'] = 'old'

    # [common] replace 'm -' with 'Metal -'
    re_word = re.compile(re.escape('m -'), re.IGNORECASE)
    raw_bc_str = re_word.sub('Metal -', raw_bc_str)

    # [common] remove extraneous words (case insensitive)
    old_extraneous_words = [
        'decommissioned',
        '2',
        '3',
        'duplicate',
    ]
    new_extraneous_words = [
        'big',
        'duplicate',
        '(upsidedown m)',
    ]

    if standardised_bc['style'] == 'new':
        for word in new_extraneous_words:
            re_word = re.compile(re.escape(word), re.IGNORECASE)
            raw_bc_str = re_word.sub('', raw_bc_str)
    else:
        for word in old_extraneous_words:
            re_word = re.compile(re.escape(word), re.IGNORECASE)
            raw_bc_str = re_word.sub('', raw_bc_str)

    # [common] ensure '/' symbols are surrounded by whitespace
    raw_bc_str = raw_bc_str.replace('/', ' / ')

    # [common] ensure whitespace is standardised to single spaces
    raw_bc_str = " ".join(raw_bc_str.split())

    # [common] identify colours (now whole words only so lightblue != blue)
    standardised_bc['colours'] = []
    for colour in COLOURS:
        if any([colour == word for word in raw_bc_str.lower().split()]):
            standardised_bc['colours'].append(colour)

    # [new] identify symbols - put all data in array, filter out other stuff
    standardised_bc['symbols'] = []

    if standardised_bc['style'] == 'new':
        raw_symbols = raw_bc_str.split()

        for raw_symbol in list(raw_symbols):
            # list(...) used so as to not delete items from currently iterating list
            # Remove any colours, 'on', '/' and '-'
            if raw_symbol.lower() in COLOURS or \
               raw_symbol.lower() == 'on' or \
               raw_symbol.lower() == '/' or \
               raw_symbol.lower() == '-':
                raw_symbols.remove(raw_symbol)

        # remove duplicates (e.g ['A', 'A'])
        standardised_bc['symbols'] = list(set(raw_symbols))

    # [common] modify LightBlue into Light Blue
    raw_bc_str = raw_bc_str.replace('LightBlue', 'Light Blue')

    # [common] string now suitably processed
    standardised_bc['name'] = raw_bc_str

    # [common] offer alternative to special characters
    standardised_bc['special'] = None
    if '◊' in standardised_bc['name']:
        standardised_bc['special'] = 'diamond'
    elif 'Σ' in standardised_bc['name']:
        standardised_bc['special'] = 'sigma'
    elif '÷' in standardised_bc['name']:
        standardised_bc['special'] = 'divides'
    elif 'θ' in standardised_bc['name']:
        standardised_bc['special'] = 'theta'

    return standardised_bc


def synchronise_BandCombo(self, transmitters_csv):
    """ Imports Band objects from data/Transmitter actions.csv """

    if hasattr(self, 'stdout'):
        self.stdout.write(self.style.MIGRATE_LABEL("\n## Band\n\n"))
        self.stdout.write("### Changes\n\n")

    transmitters_reader = csv.DictReader(
        transmitters_csv, delimiter=',', quotechar='"'
    )

    created_count = 0
    checked_count = 0
    modified_count = 0

    for row in transmitters_reader:
        if not is_valid_BandCombo(row):
            continue

        # Get associated objects
        bird = get_Bird(row)
        study_area = get_StudyArea(row)

        # Get standardised object
        band_combo_map = standardise_BandCombo(row, bird, study_area)

        try:
            band_combo = BandCombo.objects.get(bird=bird)

            # Only updated if database-stored action is older
            if band_combo.date_deployed > band_combo_map['date_deployed']:
                continue

            has_changed = False

            for key, value in band_combo_map.items():
                if getattr(band_combo, key) != value:
                    has_changed = True
                    self.stdout.write(
                        "* %s: %s changed from %s to %s" %
                        (band_combo.bird, key, getattr(band_combo, key), value)
                    )
                    setattr(band_combo, key, value)

            if has_changed:
                band_combo.full_clean()
                band_combo.save()
                modified_count += 1
            else:
                checked_count += 1

        except BandCombo.DoesNotExist:
            band_combo_map['date_imported'] = timezone.now()
            band_combo = BandCombo(**band_combo_map)
            band_combo.full_clean()
            band_combo.save()
            created_count += 1

    if hasattr(self, 'stdout'):
        self.stdout.write("\n### Results\n\n")
        self.stdout.write("* Checked: %d" % checked_count)
        self.stdout.write("* Modified: %d" % modified_count)
        self.stdout.write("* Created: %d" % created_count)
