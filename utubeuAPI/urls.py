from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from utubeuAPI.views import OwnedChatroomListCreateView, MemberChatroomListView, convert_token, InvitesCreateUpdateView



urlpatterns = [
        url(r'^ownedchatrooms$', OwnedChatroomListCreateView.as_view(), name='owned_chatrooms'),
        url(r'^memberchatrooms$', MemberChatroomListView.as_view(), name='member_chatrooms'),
        url(r'^invites$', InvitesCreateUpdateView.as_view(), name='invites'),
        url(r'^convert-token/(?P<backend>[^/]+)$', csrf_exempt(convert_token), name='convert_token'),
]