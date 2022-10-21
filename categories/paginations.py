from rest_framework import pagination


class CategorySetPagination(pagination.PageNumberPagination):
    page_size = 10
