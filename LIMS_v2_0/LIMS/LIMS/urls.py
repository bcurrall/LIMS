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

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from LIMS import views
from .views import TestPage, SampleCreate
from django.urls import path

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='startup'),
    url(r'^home/', views.home, name='home'),
    url(r'^archive/', include('archive.urls'), name='archive'),
    url(r'^project/', include('project.urls'), name='project'),
    url(r'^about/', views.about, name='about'),


    url(r'^accounts/', include('registration.backends.default.urls')), #for django-registration-redux

    url(r'^name/', views.get_name, name='your_name'),
    url(r'^thanks/', views.thanks, name='thanks'),
    url(r'^your-name/', views.your_name, name='your-name'),

    #base html
    url(r'^base/', views.base, name='base'),

    #test page for generic testing: class based
    url(r'^test/', TestPage.as_view(), name='test'),
    path('test/add/', AuthorCreate.as_view(), name='author-add'),



]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
