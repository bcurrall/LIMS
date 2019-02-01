from django.urls import path, re_path
from django.conf.urls import include, url

from . import views

app_name = 'library'

urlpatterns = [
    re_path(r'^$', views.test, name='test'),
    path(r'test/', views.test, name='test'),
    path(r'add/', views.add, name='add'),
]
