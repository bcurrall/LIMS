from django.urls import path, re_path
from django.conf.urls import include, url

from . import views

app_name = 'library'

urlpatterns = [
    re_path(r'^$', views.browser, name='browser'),
    path(r'browser/', views.browser, name='browser'),
    path(r'add/', views.add, name='add'),
    path(r'delete/', views.delete, name='delete'),
    path(r'validate/', views.validate, name='validate'),
    path(r'pool/', views.pool, name='pool'),

    path(r'test/', views.test, name='test'),

]
