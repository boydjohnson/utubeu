from django.conf.urls import url
from utubeuAPI.views import ChatroomDetailView, OwnedChatroomListCreateView, JoinableChatroomListView, MemberChatroomListView



urlpatterns = [
        url(r'^ownedchatrooms$', OwnedChatroomListCreateView.as_view(), name='owned_chatrooms'),
        url(r'^joinablechatrooms$', JoinableChatroomListView.as_view(), name='joinable_chatrooms'),
        url(r'^chatroom/(?P<pk>[0-9]+)$', ChatroomDetailView.as_view(), name='chatroom_detail'),
]