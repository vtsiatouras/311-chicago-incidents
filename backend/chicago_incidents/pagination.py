from rest_framework.pagination import PageNumberPagination


class Pagination(PageNumberPagination):
    """Pagination configuration

    See: https://www.django-rest-framework.org/api-guide/pagination/#configuration
    """
    page_size = 500
    page_size_query_param = 'per_page'
    max_page_size = 500
