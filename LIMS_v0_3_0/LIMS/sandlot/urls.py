from django.urls import include, path

from . import views

app_name = 'sandlot'

urlpatterns = [
    path('', views.AuthorTableList.as_view(), name='author_table'),
]

