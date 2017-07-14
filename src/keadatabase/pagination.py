from rest_framework import pagination

class BirdPagination(pagination.PageNumberPagination):
    page_size = 72
    page_size_query_param = 'page_size'
    max_page_size = 10000

class LocationPagination(pagination.PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 10000

class SightingPagination(pagination.PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 10000
