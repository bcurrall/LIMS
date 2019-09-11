import django_filters
from django_filters import rest_framework as filters
from .models import Library, Pool, PoolingAmount



class LibraryListFilter(filters.FilterSet):
    class Meta:
        model = Library
        fields = "__all__"

class LibraryFilter(filters.FilterSet):
    class Meta:
        model = Library
        fields = []


class PoolListFilter(filters.FilterSet):
    class Meta:
        model = Pool
        fields = "__all__"

class PoolFilter(filters.FilterSet):
    class Meta:
        model = Pool
        fields = []


class PoolingAmountListFilter(filters.FilterSet):
    class Meta:
        model = PoolingAmount
        fields = "__all__"