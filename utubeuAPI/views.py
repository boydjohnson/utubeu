from django.db.models import Q

from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateAPIView

from utubeuAPI.serializers import ChatroomSerializer, ChatroomDetailSerializer

from viewer.models import Chatroom, InvitedEmails


class OwnedChatroomListCreateView(ListCreateAPIView):
    serializer_class = ChatroomSerializer

    def get_queryset(self):
        user = self.request.user
        return Chatroom.objects.filter(owner=user.pk)


class MemberChatroomListView(ListAPIView):
    serializer_class = ChatroomSerializer

    def get_queryset(self):
        user = self.request.user
        return Chatroom.objects.filter(users=user.pk).exclude(owner=user)


class ChatroomDetailView(RetrieveUpdateAPIView):
    serializer_class = ChatroomDetailSerializer

    def get_queryset(self):
        user = self.request.user
        return Chatroom.objects.filter(Q(owner=user.pk) | Q(users=user))


class JoinableChatroomListView(ListAPIView):
    serializer_class = ChatroomSerializer

    def get_queryset(self):
        user = self.request.user
        return InvitedEmails.objects.get(user_email=user.email).exclude(chatroom__users=user.pk)

