import django_filters
from django_filters import rest_framework as filters
from .models import Library



class LibraryFilter(filters.FilterSet):

    class Meta:
        model = Library
        fields = []
