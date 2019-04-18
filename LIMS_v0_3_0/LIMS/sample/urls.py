from django.urls import path, re_path
from django.conf.urls import include, url

from . import views


app_name = 'sample'

urlpatterns = [
    # home
    re_path(r'^$', views.browser, name='home'),

    # create series
    path(r'create/', views.SampleCreateFormSetBasic.as_view(), name='create'),
    path(r'createbasic/', views.SampleCreateFormSetBasic.as_view(), name='create_basic'),
    path(r'createextract/', views.SampleCreateFormSetExtract.as_view(), name='create_extract'),
    path(r'createcellline/', views.SampleCreateFormSetCellLine.as_view(), name='create_cell'),
    path(r'createtissue/', views.SampleCreateFormSetTissue.as_view(), name='create_tissue'),
    path(r'createfull/', views.SampleCreateFormSetFull.as_view(), name='create_full'),

    # others
    path(r'browser/', views.browser, name='browser'),
    path(r'delete/', views.delete, name='delete'),
    path(r'edit/', views.edit, name='edit'),

    # testing urls
    url(r'^testview/$', views.SampleListView.as_view(), name='listview'),
    url(r'^test/$', views.test, name='test'),
    path(r'testclass/', views.TestClass.as_view(), name='testclass'),



]
