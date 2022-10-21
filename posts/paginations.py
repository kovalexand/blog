from rest_framework import pagination


class PostSetPagination(pagination.PageNumberPagination):
    page_size = 25
