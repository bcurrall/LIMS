import django_filters
from django_filters import rest_framework as filters
from .models import Sample



class SampleFilter(filters.FilterSet):

    class Meta:
        model = Sample
        fields = ['sample_name', 'sample_type']