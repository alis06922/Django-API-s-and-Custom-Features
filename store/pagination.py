from rest_framework.pagination import PageNumberPagination

# >>>> custom pagiantion
class DefaultPagination(PageNumberPagination):
    page_size = 10