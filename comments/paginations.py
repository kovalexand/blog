from rest_framework import pagination


class CommentSetPagination(pagination.PageNumberPagination):
    page_size = 15
