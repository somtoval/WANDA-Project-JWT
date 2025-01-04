from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 5  # Number of items per page
    page_size_query_param = 'page_size'  # Allow clients to set the page size
    max_page_size = 20  # Limit the maximum number of items per page
