from rest_framework import pagination
from rest_framework_gis.pagination import GeoJsonPagination

class BirdPagination(pagination.PageNumberPagination):
    page_size = 96
    page_size_query_param = 'page_size'
    max_page_size = 10000

class LocationPagination(pagination.PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 10000

class SightingPagination(pagination.PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 10000

class GridTilePagination(pagination.LimitOffsetPagination):
    default_limit = 434

class SightingGeoJSONPagination(GeoJsonPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000

class BirdSightingGeoJSONPagination(GeoJsonPagination):
    page_size = 250
    page_size_query_param = 'page_size'
    max_page_size = 10000

class GridTileGeoJSONPagination(GeoJsonPagination):
    page_size = 434
    page_size_query_param = 'page_size'
    max_page_size = 10000

class SurveyPagination(pagination.PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 10000
