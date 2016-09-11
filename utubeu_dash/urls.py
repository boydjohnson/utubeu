from django.conf.urls import url

from utubeu_dash import views as v

urlpatterns = [
    url(r'^dashboard$', v.dashboard, name='dashboard')
    ]