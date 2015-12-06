from rest_framework.generics import ListCreateAPIView, ListAPIView

from utubeuAPI.serializers import ChatroomSerializer

from viewer.models import Chatroom, InvitedEmails


class OwnedChatroomListCreate(ListCreateAPIView):
    serializer_class = ChatroomSerializer

    def get_queryset(self):
        user = self.request.user
        return Chatroom.objects.filter(owner=user)

class MemberChatroomList(ListCreateAPIView):
    serializer_class = ChatroomSerializer

    def get_queryset(self):
        user = self.request.user
        return Chatroom.objects.filter(users=user).exclude(owner=user)

    def create(self, request, *args, **kwargs):


class JoinableChatroomList(ListAPIView):
    serializer_class = ChatroomSerializer

    def get_queryset(self):
        user = self.request.user
        return InvitedEmails.objects.get(user_email=user.email).exclude(chatroom__users=user)

