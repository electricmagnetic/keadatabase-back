import io

from django.core import management
from django.conf import settings
from django.core.files.storage import default_storage

from sightings.importobservations import import_Observation

class Command(management.BaseCommand):
    help = 'Allows the import of observations data from CSVs.'

    def do_import(self):
        """ Imports objects into database """
        self.stdout.write(self.style.MIGRATE_HEADING('\nBeginning import:'))

        if settings.DEFAULT_FILE_STORAGE == 'storages.backends.s3boto3.S3Boto3Storage':
            with default_storage.open('data/observations.csv', 'r') as observations_csv_bin:
                # boto3 opens files as binary, hence the need to convert
                observations_csv = io.StringIO(observations_csv_bin.read().decode('utf-8'))

                import_Observation(self, observations_csv)
        else:
            with open('../data/observations.csv', 'rt') as observations_csv:
                import_Observation(self, observations_csv)

        self.stdout.write(self.style.SUCCESS('\nImport complete'))

    def handle(self, *args, **options):
        self.stdout.write('\nUsing input data from: %s' % settings.DEFAULT_FILE_STORAGE)

        confirm = input('\nReady to import? Type \'yes\' to continue: ')
        #confirm = 'yes' # for debugging

        if confirm == 'yes':
            self.do_import()
        else:
            self.stdout.write('\nImport cancelled!')
