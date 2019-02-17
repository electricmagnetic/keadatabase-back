import io

from django.core import management
from django.conf import settings
from django.core.files.storage import default_storage

from sightings.importsightings import import_SightingsSighting

class Command(management.BaseCommand):
    help = 'Allows the import of sightings data from CSVs.'

    def do_import(self):
        """ Imports objects into database """
        self.stdout.write(self.style.MIGRATE_HEADING('\nBeginning import:'))

        if settings.DEFAULT_FILE_STORAGE == 'storages.backends.s3boto3.S3Boto3Storage':
            with default_storage.open('data/sightings.csv', 'r') as sightings_csv_bin:
                # boto3 opens files as binary, hence the need to convert
                sightings_csv = io.StringIO(sightings_csv_bin.read().decode('utf-8'))

                import_SightingsSighting(self, sightings_csv)
        else:
            with open('../data/sightings.csv', 'rt') as sightings_csv:
                import_SightingsSighting(self, sightings_csv)

        self.stdout.write(self.style.SUCCESS('\nImport complete'))

    def handle(self, *args, **options):
        self.stdout.write('\nUsing input data from: %s' % settings.DEFAULT_FILE_STORAGE)

        confirm = input('\nReady to import? Type \'yes\' to continue: ')
        #confirm = 'yes' # for debugging

        if confirm == 'yes':
            self.do_import()
        else:
            self.stdout.write('\nImport cancelled!')
