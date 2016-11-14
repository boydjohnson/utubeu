from django.conf.urls import url
from utubeuAPI import views as api_views



urlpatterns = [
        url(r'^ownedchatrooms$', api_views.OwnedChatroomListCreateView.as_view(), name='owned_chatrooms'),
        url(r'^memberchatrooms$', api_views.MemberChatroomListView.as_view(), name='member_chatrooms'),
        url(r'^publicchatrooms$', api_views.PublicChatroomListView.as_view(), name='public_chatrooms'),
        url(r'^username$', api_views.UserInfoGetUpdateView.as_view(), name='update_username'),
        url(r'^searchchatrooms$', api_views.ChatroomSearchView.as_view(actions={'get': 'list'}), name='search_chatrooms')
]