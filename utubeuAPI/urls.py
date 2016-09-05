from django.conf.urls import url
from utubeuAPI.views import OwnedChatroomListCreateView, MemberChatroomListView



urlpatterns = [
        url(r'^ownedchatrooms$', OwnedChatroomListCreateView.as_view(), name='owned_chatrooms'),
        url(r'^memberchatrooms$', MemberChatroomListView.as_view(), name='member_chatrooms'),
]