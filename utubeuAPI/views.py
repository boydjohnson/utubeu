from django.db.models import Q

from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated


from utubeuAPI.serializers import ChatroomSerializer, ChatroomDetailSerializer
from utubeuAPI.pagination import PublicChatroomPagination
from utubeu_viewer.models import Chatroom


class OwnedChatroomListCreateView(ListCreateAPIView):
    """Can list the chatrooms a user owns and create new chatrooms"""
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        user = self.request.user
        return Chatroom.objects.filter(owner=user.pk)

    def get_serializer_class(self):
        return ChatroomSerializer


class MemberChatroomListView(ListAPIView):
    serializer_class = ChatroomDetailSerializer
    permission_classes = (IsAuthenticated, )
    def get_queryset(self):
        user = self.request.user
        return Chatroom.objects.filter(joiners=user.pk)


class PublicChatroomListView(ListAPIView):
    serializer_class = ChatroomDetailSerializer
    permission_classes = (IsAuthenticated, )
    pagination_class = PublicChatroomPagination

    def get_queryset(self):
        return Chatroom.objects.filter(~Q(owner=self.request.user.pk),is_public=True)

