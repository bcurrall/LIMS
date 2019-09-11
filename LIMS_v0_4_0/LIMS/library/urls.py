from django.urls import path, re_path
from django.conf.urls import include, url

from . import views

app_name = 'library'

urlpatterns = [
    #library home
    re_path(r'^$', views.LibraryTableSimpleView.as_view(), name='home'),

    ##library
    #library browser
    path(r'browser/', views.LibraryTableSimpleView.as_view(), name='browser'),
    path(r'browserplate/', views.LibraryTablePlateSetupView.as_view(), name='browser_plate'),
    path(r'browserqc/', views.LibraryTableQCView.as_view(), name='browser_qc'),
    path(r'browserfull/', views.LibraryTableFullView.as_view(), name='browser_full'),
    #Library create
    path(r'create/', views.LibraryCreateFormSetBasic.as_view(), name='create'),
    #Library update
    path(r'updateplate/', views.LibraryUpdateFormSetPlateSetup.as_view(), name='update_plate'),
    path(r'updateqc/', views.LibraryUpdateFormSetQC.as_view(), name='update_qc'),
    #Library delete
    path(r'librarydelete/', views.LibraryTableDeleteBase.as_view(), name='library_delete'),

    ##Pool
    #pool browser
    path(r'pool_browser/', views.PoolTableSimple.as_view(), name='pool_browser'),
    # create pool and update pooling
    path(r'pooling/', views.PoolUpdateFormSetPooling.as_view(), name='pooling'),
    # pool delete
    path(r'pooldelete/', views.PoolTableDeleteBase.as_view(), name='pool_delete'),

    ###poolingamount
    #poolingamount browser
    path(r'poolingamountbrowser/', views.PoolingAmountTableSimple.as_view(), name='pooling_amount_browser'),
    #poolingamount update
    path(r'poolingamountupdate/', views.PoolingAmountUpdateFormSetPooling.as_view(), name='pooling_amount_update'),

    #poolingamount delete
    path(r'poolingamountdelete/', views.PoolAmountTableDeleteBase.as_view(), name='pooling_amount_delete'),

    #test urls


    #archived urls
    path(r'add/', views.add, name='add'),
    path(r'delete/', views.delete, name='delete'),
    path(r'delete_pool/', views.delete_pool, name='delete_pool'),
    path(r'validate/', views.validate, name='validate'),
    path(r'pool/', views.pool, name='pool'),
    # path(r'pool_browser/', views.pool_browser, name='pool_browser'),
    path(r'edit/', views.edit, name='edit'),




]
