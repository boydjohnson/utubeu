from rest_framework.pagination import PageNumberPagination


class PublicChatroomPagination(PageNumberPagination):
    page_size = 8

