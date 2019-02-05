import django_filters
from django_filters import rest_framework as filters
from .models import Library, Pool



class LibraryFilter(filters.FilterSet):

    class Meta:
        model = Library
        fields = []


class PoolFilter(filters.FilterSet):

    class Meta:
        model = Pool
        fields = []

