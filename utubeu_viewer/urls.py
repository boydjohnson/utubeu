from django.conf.urls import url

from utubeu_viewer import views as v
from utubeu_dash import views as dash_v

urlpatterns = [
    url(r'^logout/$', v.logout, name='logout'),
    url(r'^chatroom/(?P<chatroom>[0-9A-Za-z]+)/$', v.enter_chatroom, name='enter_chatroom'),
    url(r'^splash/(?P<chatroom>[0-9A-Za-z]+)/$', v.get_splash, name='splash'),
    url(r'^dashboard$', dash_v.dashboard, name='dashboard'),
    url(r'^$', v.main_page, name='main_page')
]