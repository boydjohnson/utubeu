from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'developAdmin/', include(admin.site.urls)),
    url(r'social/', include('social.apps.django_app.urls',namespace='social')),
    url(r'api/', include('utubeuAPI.urls', namespace='api')),
    url(r'auth/', include('rest_framework_social_oauth2.urls')),
    url(r'', include('viewer.urls', namespace='viewer')),
]
