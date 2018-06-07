import io, tempfile

from django.core import management
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.utils import LayerMapping

from locations.models import Place

class Command(management.BaseCommand):
    help = 'Allows the import of NZ Place Names'

    def check_current_status(self):
        """ Outputs information about objects currently in database """
        self.stdout.write(self.style.MIGRATE_HEADING('Current status:'))
        self.stdout.write('Place: %d' % Place.objects.count())

    def do_import(self):
        """ Imports objects into database """
        self.stdout.write(self.style.MIGRATE_HEADING('\nBeginning import:'))

        place_mapping = {
            'name_id' : 'name_id',
            'name' : 'name',
            'feat_type' : 'feat_type',
            'land_district' : 'land_distr',
            # 'lon': 'crd_longit',
            # 'lat': 'crd_latitu'
            'point': 'POINT'
        }

        place_shp = '../data/lds-nz-place-names-nzgb-SHP/nz-place-names-nzgb.shp'

        lm = LayerMapping(
            Place, place_shp, place_mapping,
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
