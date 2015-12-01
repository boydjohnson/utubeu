from django.conf.urls import url


urlpatterns = [
    url(r'/$', 'viewer.views.login', name='login'),
    url(r'logout', 'viewer.views.logout', name='logout'),
    url(r'chatroom/(?P<chatroom>[0-9]+)/$', 'viewer.views.enter_chatroom', name='enter_chatroom'),
    url(r'create-chatroom/$', 'viewer.views.create_chatroom', name='create_chatroom')
]