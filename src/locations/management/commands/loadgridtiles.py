import io, tempfile

from django.core import management
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.utils import LayerMapping

from locations.models import GridTile

class Command(management.BaseCommand):
    help = 'Allows the import of kea survey grid tiles'

    def check_current_status(self):
        """ Outputs information about objects currently in database """
        self.stdout.write(self.style.MIGRATE_HEADING('Current status:'))
        self.stdout.write('GridTile: %d' % GridTile.objects.count())

    def do_import(self):
        """ Imports objects into database """
        self.stdout.write(self.style.MIGRATE_HEADING('\nBeginning import:'))

        GridTile_polygon_mapping = {
            'id' : 'id',
            'polygon': 'POLYGON'
        }
        GridTile_min_mapping = {
            'id' : 'id',
            'min': 'POINT'
        }
        GridTile_max_mapping = {
            'id' : 'id',
            'max': 'POINT'
        }

        GridTile_polygon_shp = '../data/GridTiles/Polygon.shp'
        GridTile_min_shp = '../data/GridTiles/Min.shp'
        GridTile_max_shp = '../data/GridTiles/Max.shp'

        lm_polygon = LayerMapping(
            GridTile, GridTile_polygon_shp, GridTile_polygon_mapping,
            transform=False, encoding='utf-8',
        )
        lm_polygon.save(strict=True, verbose=False)

        lm_min = LayerMapping(
            GridTile, GridTile_min_shp, GridTile_min_mapping,
            transform=False, encoding='utf-8', unique='id',
        )
        lm_min.save(strict=True, verbose=False)

        lm_max = LayerMapping(
            GridTile, GridTile_max_shp, GridTile_max_mapping,
            transform=False, encoding='utf-8', unique='id',
        )
        lm_max.save(strict=True, verbose=False)

        self.stdout.write(self.style.SUCCESS('\nImport complete'))

    def handle(self, *args, **options):
        self.check_current_status()

        confirm = input('\nReady to import? Type \'yes\' to continue: ')
        #confirm = 'yes' # for debugging

        if confirm == 'yes':
            self.do_import()
        else:
            self.stdout.write('\nImport cancelled!')
