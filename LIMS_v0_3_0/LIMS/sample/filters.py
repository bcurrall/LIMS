import django_filters
from django_filters import rest_framework as filters
from .models import Sample



class SampleFilter(filters.FilterSet):

    class Meta:
        model = Sample
        fields = {
            'project_name': ['icontains'],
            'sample_name': ['icontains'],
            'sample_type': ['exact'],
        }
