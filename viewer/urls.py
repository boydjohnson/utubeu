from django.conf.urls import url


urlpatterns = [
    url(r'', 'viewer.views.login', name='login'),
    url(r'logout', 'viewer.views.logout', name='logout'),
]