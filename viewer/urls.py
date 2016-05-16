from django.conf.urls import url


urlpatterns = [
    url(r'^logout/$', 'viewer.views.logout', name='logout'),
    url(r'^chatroom/(?P<chatroom>[0-9]+)/$', 'viewer.views.enter_chatroom', name='enter_chatroom'),
    url(r'^dashboard$', 'viewer.views.dashboard', name='dashboard')
]