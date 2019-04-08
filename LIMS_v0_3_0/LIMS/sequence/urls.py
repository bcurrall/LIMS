from django.urls import path, re_path
from django.conf.urls import include, url

from . import views

app_name = 'sequence'

urlpatterns = [
    re_path(r'^$', views.test, name='home'),
    path(r'browser/', views.browser, name='browser'),
    path(r'add_wus_sub/', views.add_wus_sub, name='add_wus_sub'),
    path(r'edit/', views.edit, name='edit'),
    path(r'delete/', views.delete, name='delete'),

    path(r'test/', views.test, name='test'),

]
