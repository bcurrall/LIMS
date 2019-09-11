import django_filters
from django_filters import rest_framework as filters
from .models import Sample

class SampleListFilter(filters.FilterSet):
    class Meta:
        model = Sample
        fields = "__all__"

