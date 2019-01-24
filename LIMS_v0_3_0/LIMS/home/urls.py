from django.urls import path
from django.conf.urls import include, url

from . import views

app_name = 'home'

urlpatterns = [
    # /home/
    url(r'^', views.index, name='index'),
]
