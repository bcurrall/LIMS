from django.urls import path, re_path
from django.conf.urls import include, url


from . import views


app_name = 'sample'

urlpatterns = [
    # home
    re_path(r'^$', views.browser, name='home'),

    # create series
    path(r'create/', views.SampleCreateFormSetBasic.as_view(), name='create'),
    path(r'createextract/', views.SampleCreateFormSetExtract.as_view(), name='create_extract'),
    path(r'createcellline/', views.SampleCreateFormSetCellLine.as_view(), name='create_cell'),
    path(r'createtissue/', views.SampleCreateFormSetTissue.as_view(), name='create_tissue'),
    path(r'createfull/', views.SampleCreateFormSetFull.as_view(), name='create_full'),

    # table view series
    url(r'browser/', views.SampleTableList.as_view(), name='browser'),
    url(r'browserfreezer/', views.SampleFreezerTableList.as_view(), name='browser_freezer'),
    url(r'browserfull/', views.SampleFullTableList.as_view(), name='browser_full'),

    # update series
    path(r'update/', views.SampleUpdateFormSetBasic.as_view(), name='update'),
    path(r'updateextract/', views.SampleUpdateFormSetExtract.as_view(), name='update_extract'),
    path(r'updatecellline/', views.SampleUpdateFormSetCellLine.as_view(), name='update_cell'),
    path(r'updatetissue/', views.SampleUpdateFormSetTissue.as_view(), name='update_tissue'),
    path(r'updatefull/', views.SampleUpdateFormSetFull.as_view(), name='update_full'),


    # others
    # path(r'browser/', views.browser, name='browser'),
    path(r'delete/', views.delete, name='delete'),
    path(r'edit/', views.edit, name='edit'),

    # testing urls
    url(r'^testview/$',views.SampleTableList.as_view() , name='listview'),
    url(r'^test/$', views.test, name='test'),
    path(r'testclass/', views.TestClass.as_view(), name='testclass'),



]
