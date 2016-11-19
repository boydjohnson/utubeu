from rest_framework.pagination import PageNumberPagination


class ChatroomPagination(PageNumberPagination):
    page_size = 8


class ManyChatroomPagination(PageNumberPagination):
    page_size = 20