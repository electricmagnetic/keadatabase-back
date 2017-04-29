import csv
import datetime

from django.utils.text import slugify
from django.core.management import BaseCommand

from keadatabase.choices import *
from birds.models import Bird
from locations.models import AreaLocation
from bands.models import Band, BandCombo


class Command(BaseCommand):
    help = "Allows the import of information exported from the primary Access-based database."


    def check_current_status(self):
        """ Outputs information about objects currently in database """
        self.stdout.write(self.style.MIGRATE_LABEL("\n  Current data status:"))
        self.stdout.write("    Areas: %d" % AreaLocation.objects.count())
        self.stdout.write("    Birds: %d" % Bird.objects.count())
        self.stdout.write("    Bands: %d" % Band.objects.count())
        self.stdout.write("    Band Combos: %d" % BandCombo.objects.count())


    def import_areas(self):
        """ Imports AreaLocation objects from data/areas.csv """
        self.stdout.write(self.style.MIGRATE_LABEL("\n  Importing areas..."))

        with open('data/areas.csv', 'rt') as areas_csv:
            areas_reader = csv.DictReader(areas_csv, delimiter=',', quotechar='"')

            created_count = 0
            checked_count = 0

            for row in areas_reader:
                # Generate slug
                name_slugified = slugify(row['Study area'])

                # Map fields
                area_map = {
                    'slug': name_slugified,
                    'name': row['Study area'],
                }

                # TODO: check duplicates
                # TODO: relations

                # Save as AreaLocation object
                try:
                    area = AreaLocation.objects.get(slug=name_slugified)
                    for key, value in area_map.items():
                        setattr(area, key, value)
                    area.full_clean()
                    area.save()
                    checked_count += 1
                except AreaLocation.DoesNotExist:
                    area = AreaLocation(**area_map)
                    area.full_clean()
                    area.save()
                    created_count += 1

        self.stdout.write("    Checked: %d" % checked_count)
        self.stdout.write("    New: %d" % created_count)
        self.stdout.write("    ...done!")


    def import_bands(self):
        """ Imports Band objects from various csv files """
        self.stdout.write(self.style.MIGRATE_LABEL("\n  Importing bands..."))
        self.stdout.write("    ...TODO!")


    def import_birds(self):
        """ Imports Bird objects from data/birds.csv """
        self.stdout.write(self.style.MIGRATE_LABEL("\n  Importing birds..."))

        with open('data/birds.csv', 'rt') as birds_csv:
            birds_reader = csv.DictReader(birds_csv, delimiter=',', quotechar='"')

            created_count = 0
            checked_count = 0

            for row in birds_reader:
                # Validate species
                if row['Species'] != 'Kea':
                    continue

                # Format and validate status
                status_map = {
                    'Alive': '+',
                    'Dead': '-',
                    'Missing': '',
                    'Unknown': '',
                    'Not sure, it\'s been over a year': '',
                }
                if row['Status'] not in status_map:
                    continue

                # Format and validate sex
                sex_map = {
                    'Male': 'M',
                    'Female': 'F',
                    'Undetermined': '',
                }
                if row['Sex'] not in sex_map:
                    continue

                # Format birthday
                if row['birthday']:
                    birthday_formatted = datetime.datetime.strptime(row['birthday'],
                                                                    "%d/%m/%Y %H:%M:%S")
                else:
                    birthday_formatted = None

                # Generate slug
                name_slugified = slugify(row['Kea ID'])

                # Get associated area
                area = AreaLocation.objects.get(name=row['Study Area'])
                # TODO: not all areas have associated AreaLocations

                # Map fields
                bird_map = {
                    'slug': name_slugified,
                    'name': row['Kea ID'],
                    'sex': sex_map[row['Sex']],
                    'status': status_map[row['Status']],
                    'birthday': birthday_formatted,
                    'area': area,
                    #'photo': '',
                    #'date_imported': '',
                }

                #self.stdout.write("%s" % (row['Study area']))
                # TODO: media
                # TODO: relations


                # Attempts to get object (on unique slug).
                #   If exists: update existing values
                #   If doesn't exist: create new bird
                try:
                    bird = Bird.objects.get(slug=name_slugified)
                    for key, value in bird_map.items():
                        setattr(bird, key, value)
                    bird.full_clean()
                    bird.save()
                    checked_count += 1
                except Bird.DoesNotExist:
                    bird = Bird(**bird_map)
                    bird.full_clean()
                    bird.save()
                    created_count += 1


        self.stdout.write("    Checked: %d" % checked_count)
        self.stdout.write("    New: %d" % created_count)
        self.stdout.write("    ...done!")


    def do_import(self):
        """ Imports objects into database """
        self.stdout.write(self.style.MIGRATE_HEADING("\nBeginning import..."))

        self.import_areas()
        self.import_bands()
        self.import_birds()

        self.stdout.write(self.style.SUCCESS("\nImport successful!"))


    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING("Database import"))
        self.check_current_status()

        #confirm = input("\nReady to import? Type 'yes' to continue, or 'no' to cancel: ")
        confirm = 'yes' # for debugging

        if confirm == 'yes':
            self.do_import()
        else:
            self.stdout.write("\nImport cancelled!")
