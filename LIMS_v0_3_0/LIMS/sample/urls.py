from django.urls import path, re_path
from django.conf.urls import include, url

from . import views

app_name = 'sample'

urlpatterns = [
    re_path(r'^$', views.browser, name='home'),
    path(r'add/', views.add, name='add'),
    path(r'browser/', views.browser, name='browser'),
    path(r'delete/', views.delete, name='delete'),
    path(r'edit/', views.edit, name='edit'),

    url(r'^test/$', views.test, name='test'),
    path(r'testclass/', views.TestClass.as_view(), name='testclass'),
    path(r'create/', views.SampleCreateTest.as_view(), name='create'),
    path(r'createformsettest/', views.CreateFormSet.as_view(), name='createformsettest'),
    path(r'samplecreateformsettest/', views.SampleCreateFormSet.as_view(), name='samplecreateformsettest'),


]
