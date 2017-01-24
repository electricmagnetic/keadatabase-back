import csv
import datetime

from django.core.management import BaseCommand

from keadatabase.choices import *
from birds.models import Bird
from bands.models import Band, BandCombo


class Command(BaseCommand):
    help = "Allows the import of information exported from the primary Access-based database."

    def check_current_status(self):
        """ Outputs information about objects currently in database """
        birds = Bird.objects.count()
        bands = Band.objects.count()
        band_combos = BandCombo.objects.count()

        self.stdout.write(self.style.MIGRATE_LABEL("\n  Current data status:"))
        self.stdout.write("    Birds: %d" % birds)
        self.stdout.write("    Bands: %d" % bands)
        self.stdout.write("    Band Combos: %d" % band_combos)


    def check_import_status(self):
        """ Outputs information about objects to be imported """
        self.stdout.write(self.style.MIGRATE_LABEL("\n  Import data status:"))
        self.stdout.write("    TODO: checking import data")


    def import_areas(self):
        """ Imports AreaLocation objects from data/areas.csv """
        self.stdout.write("  Importing areas...")
        self.stdout.write("TODO")
        self.stdout.write("    ...done!")


    def import_birds(self):
        """ Imports Bird objects from data/birds.csv """
        self.stdout.write("  Importing birds...")

        with open('data/birds.csv', 'rt') as birds_csv:
            birds_reader = csv.DictReader(birds_csv, delimiter=',', quotechar='"')
            for row in birds_reader:
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
                    birthday_formatted = datetime.datetime.strptime(row['birthday'], "%d/%m/%y %H:%M:%S")
                else:
                    birthday_formatted = None

                # Map fields
                bird_map = {
                    'name': row['Kea ID'],
                    'sex': sex_map[row['Sex']],
                    'status': status_map[row['Status']],
                    'birthday': birthday_formatted,
                    #'area': '',
                    #'photo': '',
                    #'date_imported': '',
                }

                # TEMP: #self.stdout.write("%s: %s %s %s" % (row['Kea ID'], row['Study area'], row['birthday'], birthday_formatted))
                # TODO: check duplicates

                # Save as Bird object
                bird = Bird(**bird_map)
                bird.full_clean()
                bird.save()

        self.stdout.write("    ...done!")



    def do_import(self):
        """ Imports objects into database """
        self.stdout.write(self.style.MIGRATE_HEADING("\nBeginning import..."))

        self.import_areas()
        #self.stdout.write("TODO: importing bands")
        self.import_birds()

        self.stdout.write(self.style.SUCCESS("\nImport successful!"))


    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING("Database import"))
        self.check_current_status()
        self.check_import_status()

        confirm = input("\nReady to import? Type 'yes' to continue, or 'no' to cancel: ")
        # TEMP: confirm = 'yes'

        if confirm == 'yes':
            self.do_import()
        else:
            self.stdout.write("\nImport cancelled!")
