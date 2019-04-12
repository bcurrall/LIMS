from django.urls import path, re_path
from django.conf.urls import include, url

from . import views


app_name = 'sample'

urlpatterns = [
    re_path(r'^$', views.browser, name='home'),

    # create series
    path(r'create/', views.SampleCreateFormSetBasic.as_view(), name='create'),
    path(r'createbasic/', views.SampleCreateFormSetBasic.as_view(), name='create_basic'),
    path(r'createhumantissue/', views.SampleCreateFormSetHumanTissue.as_view(), name='create_human_tissue'),
    path(r'createfull/', views.SampleCreateFormSetFull.as_view(), name='create_full'),
    path(r'browser/', views.browser, name='browser'),
    path(r'delete/', views.delete, name='delete'),
    path(r'edit/', views.edit, name='edit'),

    url(r'^test/$', views.test, name='test'),
    path(r'testclass/', views.TestClass.as_view(), name='testclass'),
    path(r'genericcreateformset/', views.GenericCreateFormSet.as_view(), name='GenericCreateFormSet'),



]
