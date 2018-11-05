__author__ = "Benjamin B. Currall"
__license__ = "GPL"
__version__ = "1.0.1"
__email__ = "benjamincurrall@gmail.com"
__maintainer__ = "Benjamin B. Currall"
__status__ = "Production"

"""talkLims URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from django.conf.urls import url


from . import views

urlpatterns =[
    url(r'^$', views.archive, name='index'),

    ### adds

    #add samples
    url(r'^add_full_sample_single/$', views.add_full_sample_single, name='add_full_sample_single'),
    url(r'^add_sample_single/$', views.add_sample_single, name='add_sample_single'),
    url(r'^add_individual_single/', views.add_individual_single, name='add_individual_single'),
    url(r'^add_full_sample_multiple/$', views.add_full_sample_multiple, name='add_full_sample_multiple'),
    url(r'^add_sample_multiple/$', views.add_sample_multiple, name='add_sample_multiple'),
    url(r'^add_individual_multiple/$', views.add_individual_multiple, name='add_individual_multiple'),




    ### validate
    url(r'^validate_sample_multiple/$', views.validate_sample_multiple, name='validate_sample_multiple'),
    url(r'^validate_individual_multiple/$', views.validate_individual_multiple, name='validate_individual_multiple'),
    url(r'^validate_freezer/$', views.validate_freezer, name='validate_freezer'),


    ### edits

    # edit
    url(r'^edit_sample_single/(?P<id>\d+)/$', views.edit_sample_single, name='edit_sample_single'),
    url(r'^edit_sample_multiple/$', views.edit_sample_multiple, name='edit_sample_multiple'),
    url(r'^edit_individual_multiple/$', views.edit_individual_multiple, name='edit_individual_multiple'),


    # delete samples
    url(r'^delete_sample/(?P<id>\d+)/$', views.delete_sample, name='delete_sample'),
    url(r'^delete_sample_multiple/$', views.delete_sample_multiple, name='delete_sample_multiple'),
    url(r'^delete_individual_multiple/$', views.delete_individual_multiple, name='delete_individual_multiple'),

    # delete freezers

    # delete boxes


    # freezers and boxes
    url(r'^add_freezer/$', views.add_freezer, name='add_freezer'),
    url(r'^add_box/$', views.add_box, name='add_box'),

    # test
    url(r'^export/$', views.export, name='export'),
    url(r'^export/$', views.export, name='export'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^import_data/$', views.import_data, name='import_data'),
    url(r'^simple_upload/$', views.simple_upload, name='simple_upload'),
    url(r'^model_form_upload/$', views.model_form_upload, name='model_form_upload'),



]