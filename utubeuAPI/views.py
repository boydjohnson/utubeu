from oauth2_provider.ext.rest_framework.authentication import OAuth2Authentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import ListCreateAPIView, ListAPIView

from rest_framework.permissions import IsAuthenticated

from utubeuAPI.serializers import ChatroomSerializer, ChatroomDetailSerializer
from utubeu_viewer.models import Chatroom


class OwnedChatroomListCreateView(ListCreateAPIView):
    """Can list the chatrooms a user owns and create new chatrooms"""
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Chatroom.objects.filter(owner=user.pk)

    def get_serializer_class(self):
        return ChatroomSerializer


class MemberChatroomListView(ListAPIView):
    serializer_class = ChatroomDetailSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Chatroom.objects.filter(joiners=user.pk)