import io, tempfile, csv

from django.core import management
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.utils import LayerMapping

from locations.models import GridTile


class Command(management.BaseCommand):
    help = 'Allows the import of kea survey grid tiles'

    def import_geometries(self):
        """ Does the import of geometries """

        GridTile_polygon_mapping = {'id': 'id', 'polygon': 'POLYGON'}
        GridTile_min_mapping = {'id': 'id', 'min': 'POINT'}
        GridTile_max_mapping = {'id': 'id', 'max': 'POINT'}
        GridTile_centroid_mapping = {
            'id': 'id',
            'centroid': 'POINT',
        }

        GridTile_polygon_shp = '../data/GridTiles/Polygon.shp'
        GridTile_min_shp = '../data/GridTiles/Min.shp'
        GridTile_max_shp = '../data/GridTiles/Max.shp'
        GridTile_centroid_shp = '../data/GridTiles/Centroid.shp'

        lm_polygon = LayerMapping(
            GridTile,
            GridTile_polygon_shp,
            GridTile_polygon_mapping,
            transform=False,
            encoding='utf-8',
        )
        lm_polygon.save(strict=True, verbose=False)

        lm_min = LayerMapping(
            GridTile,
            GridTile_min_shp,
            GridTile_min_mapping,
            transform=False,
            encoding='utf-8',
            unique='id',
        )
        lm_min.save(strict=True, verbose=False)

        lm_max = LayerMapping(
            GridTile,
            GridTile_max_shp,
            GridTile_max_mapping,
            transform=False,
            encoding='utf-8',
            unique='id',
        )
        lm_max.save(strict=True, verbose=False)

        lm_centroid = LayerMapping(
            GridTile,
            GridTile_centroid_shp,
            GridTile_centroid_mapping,
            transform=False,
            encoding='utf-8',
            unique='id',
        )
        lm_centroid.save(strict=True, verbose=False)

    def import_neighbours(self):
        """ Import neighbours information from a standard CSV file """

        GridTile_neighbours_csv = '../data/GridTiles/neighbours.csv'

        neighbours_reader = csv.DictReader(
            open(GridTile_neighbours_csv, 'rt'), delimiter=',', quotechar='"'
        )

        for row in neighbours_reader:
            # Obtain fields (tile has to exclude self from neighbours)
            id = row['grid_id']
            neighbours = [
                neighbour for neighbour in row['neighbours'].split(',')
                if not (id in neighbour)
            ]

            # Map fields
            grid_tile_map = {
                'id': id,
                'neighbours': neighbours,
            }

            # Save as GridTile object
            grid_tile = GridTile.objects.get(pk=id)

            for key, value in grid_tile_map.items():
                setattr(grid_tile, key, value)

            grid_tile.full_clean()
            grid_tile.save()

    def check_current_status(self):
        """ Outputs information about objects currently in database """
        self.stdout.write(self.style.MIGRATE_HEADING('Current status:'))
        self.stdout.write('GridTile: %d' % GridTile.objects.count())

    def do_import(self):
        """ Imports objects into database """
        self.stdout.write(self.style.MIGRATE_HEADING('\nBeginning import:'))

        self.import_geometries()
        self.import_neighbours()

        self.stdout.write(self.style.SUCCESS('\nImport complete'))

    def handle(self, *args, **options):
        self.check_current_status()

        confirm = input('\nReady to import? Type \'yes\' to continue: ')
        #confirm = 'yes' # for debugging

        if confirm == 'yes':
            self.do_import()
        else:
            self.stdout.write('\nImport cancelled!')
