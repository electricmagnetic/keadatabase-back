import os

from django.contrib.gis.utils import LayerMapping

from .models import PrimaryLocation


areas_mapping = {
    'name': 'Name',
    'mpoly': 'MULTIPOLYGON',
}

areas_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data',
                                         'doc-public-conservation-areas.shp'))


def run(verbose=True):
    areas_layer_mapping = LayerMapping(
        PrimaryLocation, areas_shp, areas_mapping,
        transform=False, encoding='iso-8859-1',
    )
    areas_layer_mapping.save(strict=True, verbose=verbose)
