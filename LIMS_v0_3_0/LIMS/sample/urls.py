from django.urls import path, re_path
from django.conf.urls import include, url

from . import views

app_name = 'sample'

urlpatterns = [
    re_path(r'^$', views.browser, name='browser'),
    path(r'add/', views.add, name='add'),
    url(r'^test/$', views.test, name='test'),
    url(r'^delete/$', views.delete, name='delete'),

]
