import io

from django.core import management
from django.conf import settings
from django.core.files.storage import default_storage

from synchronise.locations import synchronise_StudyArea
from synchronise.birds import synchronise_Bird
from synchronise.bands import synchronise_BandCombo
from locations.models import StudyArea
from birds.models import Bird
from bands.models import BandCombo


class Command(management.BaseCommand):
    help = 'Allows the import of tables exported from the Access database.'

    def check_current_status(self):
        """ Outputs information about objects currently in database """
        self.stdout.write(self.style.MIGRATE_HEADING('# Current status\n\n'))
        self.stdout.write('* StudyArea: %d' % StudyArea.objects.count())
        self.stdout.write('* Bird: %d' % Bird.objects.count())
        self.stdout.write('* BandCombo: %d' % BandCombo.objects.count())

    def do_import(self):
        """ Imports objects into database """
        self.stdout.write(self.style.MIGRATE_HEADING('\n# Beginning import\n'))

        if settings.DEFAULT_FILE_STORAGE == 'storages.backends.s3boto3.S3Boto3Storage':
            with default_storage.open('data/tStudyAreas.csv', 'r') as areas_csv_bin, \
                 default_storage.open('data/Kea.csv', 'r') as birds_csv_bin, \
                 default_storage.open('data/Transmitter actions.csv', 'r') as transmitters_csv_bin:

                # boto3 opens files as binary, hence the need to convert
                areas_csv = io.StringIO(areas_csv_bin.read().decode('utf-8'))
                birds_csv = io.StringIO(birds_csv_bin.read().decode('utf-8'))
                transmitters_csv = io.StringIO(
                    transmitters_csv_bin.read().decode('utf-8')
                )

                synchronise_StudyArea(self, areas_csv)
                synchronise_Bird(self, birds_csv)
                synchronise_BandCombo(self, transmitters_csv)
        else:
            with open('../data/tStudyAreas.csv', 'rt') as areas_csv, \
                 open('../data/Kea.csv', 'rt') as birds_csv, \
                 open('../data/Transmitter actions.csv', 'rt') as transmitters_csv:

                synchronise_StudyArea(self, areas_csv)
                synchronise_Bird(self, birds_csv)
                synchronise_BandCombo(self, transmitters_csv)

        self.stdout.write(self.style.SUCCESS('\n*Import complete!*'))

    def handle(self, *args, **options):
        self.check_current_status()

        self.stdout.write(
            '\nUsing input data from: %s' % settings.DEFAULT_FILE_STORAGE
        )

        confirm = input('\nReady to import? Type \'yes\' to continue: ')
        #confirm = 'yes' # for debugging

        if confirm == 'yes':
            self.do_import()
        else:
            self.stdout.write('\n*Import cancelled!*')
