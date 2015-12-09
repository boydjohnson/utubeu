from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from utubeuAPI.views import ChatroomDetailView, OwnedChatroomListCreateView, JoinableChatroomListView, MemberChatroomListView, convert_token



urlpatterns = [
        url(r'^ownedchatrooms$', OwnedChatroomListCreateView.as_view(), name='owned_chatrooms'),
        url(r'^joinablechatrooms$', JoinableChatroomListView.as_view(), name='joinable_chatrooms'),
        url(r'^memberchatrooms$', MemberChatroomListView.as_view(), name='member_chatrooms'),
        url(r'^chatroom/(?P<pk>[0-9]+)$', ChatroomDetailView.as_view(), name='chatroom_detail'),
        url(r'^convert-token/(?P<backend>[^/]+)$', csrf_exempt(convert_token), name='convert_token'),
]