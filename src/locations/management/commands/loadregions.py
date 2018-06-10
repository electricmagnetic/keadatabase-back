import io, tempfile

from django.core import management
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.utils import LayerMapping

from locations.models import Region

class Command(management.BaseCommand):
    help = 'Allows the import of regions'

    def check_current_status(self):
        """ Outputs information about objects currently in database """
        self.stdout.write(self.style.MIGRATE_HEADING('Current status:'))
        self.stdout.write('Region: %d' % Region.objects.count())

    def do_import(self):
        """ Imports objects into database """
        self.stdout.write(self.style.MIGRATE_HEADING('\nBeginning import:'))

        region_mapping = {
            'name' : 'NAME',
            'polygon': 'POLYGON'
        }

        region_shp = '../data/kx-nz-regional-councils-2012-yearly-pattern-SHP/nz-regional-councils-2012-yearly-pattern.shp'

        lm = LayerMapping(
            Region, region_shp, region_mapping,
            transform=False, encoding='utf-8',
        )
        lm.save(strict=True, verbose=False)

        self.stdout.write(self.style.SUCCESS('\nImport complete'))

    def handle(self, *args, **options):
        self.check_current_status()

        confirm = input('\nReady to import? Type \'yes\' to continue: ')
        #confirm = 'yes' # for debugging

        if confirm == 'yes':
            self.do_import()
        else:
            self.stdout.write('\nImport cancelled!')
