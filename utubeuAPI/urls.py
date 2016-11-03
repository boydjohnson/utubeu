from django.conf.urls import url
from utubeuAPI.views import OwnedChatroomListCreateView, MemberChatroomListView, PublicChatroomListView



urlpatterns = [
        url(r'^ownedchatrooms$', OwnedChatroomListCreateView.as_view(), name='owned_chatrooms'),
        url(r'^memberchatrooms$', MemberChatroomListView.as_view(), name='member_chatrooms'),
        url(r'^publicchatrooms$', PublicChatroomListView.as_view(), name='public_chatrooms')
]