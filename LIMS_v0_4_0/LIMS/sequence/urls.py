from django.urls import path, re_path
from django.conf.urls import include, url

from . import views

app_name = 'sequence'

urlpatterns = [
    #sequencing home


    ## WUSSubmission
    #WUSSubmission - browser
    path(r'browser/', views.WUSSubmissionTableSimpleView.as_view(), name='browser'),

    # WUSSubmission - create
    path(r'submissioncreate/', views.WUSSubmissionCreateFormSetPooling.as_view(), name='submission_create'),
    path(r'submissioncreate2/', views.WUSSubmissionCreateFormSetPooling.as_view(), name='submission_create2'),

    # WUSSubmission - update
    path(r'submissionupdate/', views.WUSSubmissionUpdateFormSetPooling.as_view(), name='submission_update'),

    # WUSSubmission - delete
    path(r'wussubmissiondelete/', views.WUSSubmissionTableDeleteBase.as_view(), name='submission_delete'),

    ## WUSPools
    #WUSSubmission browser
    path(r'browserpool/', views.WUSPoolTableSimpleView.as_view(), name='browser_pool'),
    # update WUSPools
    path(r'wuspools/', views.WUSPoolUpdateFormSetPooling.as_view(), name='wus_pool'),
    # WUSPool - delete
    path(r'wuspooldelete/', views.WUSPoolTableDeleteBase.as_view(), name='wuspool_delete'),

    ## WUSResult
    #WUSResult browser
    path(r'browserresult/', views.WUSResultTableSimpleView.as_view(), name='browser_result'),
    # create
    path(r'createresult/', views.WUSResultCreateFormSetBasic.as_view(), name='create_result'),
    # update
    path(r'updateresult/', views.WUSResultUpdateFormSetBasic.as_view(), name='update_result'),




    #archived
    # path(r'browserold/', views.browser, name='browser_old'),
    # re_path(r'^$', views.test, name='home'),
    # path(r'add_wus_sub/', views.add_wus_sub, name='add_wus_sub'),
    # path(r'edit/', views.edit, name='edit'),
    # path(r'delete/', views.delete, name='delete'),

    # path(r'test/', views.test, name='test'),
]
