from django.urls import path, re_path
from django.conf.urls import include, url

from . import views

app_name = 'library'

urlpatterns = [
    re_path(r'^$', views.lib_browser, name='lib_browser'),
    path(r'lib_browser/', views.lib_browser, name='lib_browser'),
    path(r'add/', views.add, name='add'),
    path(r'delete/', views.delete, name='delete'),
    path(r'validate/', views.validate, name='validate'),
    path(r'pool/', views.pool, name='pool'),
    path(r'pool_browser/', views.pool_browser, name='pool_browser'),

    path(r'test/', views.test, name='test'),

]
