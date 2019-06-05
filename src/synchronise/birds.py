import csv
import datetime

from django.utils import timezone
from django.core import management
from django.utils.text import slugify

from locations.models import StudyArea
from birds.models import Bird

status_map = {
    'Alive': 'alive',
    'Dead': 'dead',
    'Missing': 'unknown',
    'Unknown': 'unknown',
}

sex_map = {
    'Male': 'male',
    'Female': 'female',
    'Undetermined': 'undetermined',
}

def is_valid_Bird(row):
    """ Returns True if valid Bird - filters noise in original dataset """

    # Check to confirm species is listed as 'Kea' (not 'Dummy' or 'Cavity')
    if row['Species'] != 'Kea':
        return False

    # Check bird has a valid status ('Alive', 'Dead' or otherwise)
    if row['Status'] not in status_map:
        return False

    # Check bird has a valid sex ('Male', 'Female' or 'Undetermined')
    if row['Sex'] not in sex_map:
        return False

    return True

def synchronise_Bird(self, birds_csv):
    """ Imports Bird objects from data/Kea.csv """

    if hasattr(self, 'stdout'):
        self.stdout.write(self.style.MIGRATE_LABEL("\n## Bird\n\n"))
        self.stdout.write("### Changes\n\n")

    birds_reader = csv.DictReader(birds_csv, delimiter=',', quotechar='"')

    created_count = 0
    checked_count = 0
    modified_count = 0

    for row in birds_reader:
        if not is_valid_Bird(row):
            continue

        # Represent birthday as a datetime object based on input format
        if row['birthday']:
            birthday = datetime.datetime.strptime(row['birthday'],
                                                  "%Y-%m-%d %H:%M:%S").date()
        else:
            birthday = None

        # Generate slug
        name_slugified = slugify(row['Kea ID'])

        # Get associated area
        study_area = StudyArea.objects.get(name=row['Study Area'])

        # Map fields
        bird_map = {
            'slug': name_slugified,
            'name': row['Kea ID'],
            'sex': sex_map[row['Sex']],
            'status': status_map[row['Status']],
            'birthday': birthday,
            'primary_band': row['Primary band no'],
            'study_area': study_area,
        }

        try:
            bird = Bird.objects.get(slug=name_slugified)

            has_changed = False

            for key, value in bird_map.items():
                if getattr(bird, key) != value:
                    has_changed = True
                    self.stdout.write("* %s: %s changed from %s to %s" % (name_slugified, key, getattr(bird, key), value))
                    setattr(bird, key, value)

            if has_changed:
                bird.full_clean()
                bird.save()
                modified_count += 1
            else:
                checked_count += 1

        except Bird.DoesNotExist:
            bird_map['date_imported'] = timezone.now()
            bird = Bird(**bird_map)
            bird.full_clean()
            bird.save()
            created_count += 1

    if hasattr(self, 'stdout'):
        self.stdout.write("\n### Results\n\n")
        self.stdout.write("* Checked: %d" % checked_count)
        self.stdout.write("* Modified: %d" % modified_count)
        self.stdout.write("* Created: %d" % created_count)
