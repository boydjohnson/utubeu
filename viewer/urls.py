from django.conf.urls import url


urlpatterns = [
    url(r'', 'viewer.views.login', name='login'),
]