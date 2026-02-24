from rest_framework.pagination import LimitOffsetPagination
from rest_framework.pagination import PageNumberPagination



class CustomPagination(LimitOffsetPagination):
    default_limit = 20
    max_limit = 100
    


class CatalogPagination(PageNumberPagination):
    page_size = 20