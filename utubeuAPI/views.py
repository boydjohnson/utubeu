from django.db.models import Q, ObjectDoesNotExist

from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter


from utubeuAPI.serializers import ChatroomSerializer, ChatroomDetailSerializer, UserInfoSerializer
from utubeuAPI.pagination import ChatroomPagination, ManyChatroomPagination
from utubeu_viewer.models import Chatroom, UserSiteInfo


class OwnedChatroomListCreateView(ListCreateAPIView):
    """Can list the chatrooms a user owns and create new chatrooms"""
    permission_classes = (IsAuthenticated, )
    serializer_class = ChatroomSerializer
    pagination_class = ManyChatroomPagination

    def get_queryset(self):
        user = self.request.user
        return Chatroom.objects.filter(owner=user.pk)


class MemberChatroomListView(ListAPIView):
    serializer_class = ChatroomDetailSerializer
    permission_classes = (IsAuthenticated, )
    pagination_class = ManyChatroomPagination

    def get_queryset(self):
        user = self.request.user
        return Chatroom.objects.filter(joiners=user.pk)


class PublicChatroomListView(ListAPIView):
    serializer_class = ChatroomDetailSerializer
    permission_classes = (IsAuthenticated, )
    pagination_class = ChatroomPagination

    def get_queryset(self):
        return Chatroom.objects.filter(~Q(owner=self.request.user.pk),is_public=True)


class UserInfoGetUpdateView(RetrieveUpdateAPIView):
    serializer_class = UserInfoSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        user_pk = self.request.user.pk
        try:
            user_info = UserSiteInfo.objects.get(user=user_pk)
        except ObjectDoesNotExist:
            user_info = UserSiteInfo.objects.create(user=user_pk)
        return user_info


class ChatroomSearchView(ReadOnlyModelViewSet):
    serializer_class = ChatroomDetailSerializer
    permission_classes = (IsAuthenticated, )
    pagination_class = ManyChatroomPagination
    filter_backends = (SearchFilter, )
    search_fields = ('name', 'description')

    def get_queryset(self):
        return Chatroom.objects.filter(Q(joiners=self.request.user) | Q(is_public=True))
