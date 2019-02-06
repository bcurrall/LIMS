from django.urls import path, re_path
from django.conf.urls import include, url

from . import views

app_name = 'sample'

urlpatterns = [
    re_path(r'^$', views.test, name='home'),
    path(r'test/$', views.test, name='test'),

]
