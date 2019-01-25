import django_filters
from django_filters import rest_framework as filters
from .models import Sample, Sample2, Individual, Freezer



class SampleFilter(filters.FilterSet):

    class Meta:
        model = Sample2
        fields = ['individual', 'type']


class IndividualFilter(filters.FilterSet):

    class Meta:
        model = Individual
        fields = ['project_id', 'species']

class FreezerFilter(filters.FilterSet):

    class Meta:
        model = Freezer
        fields = ['name', 'freezer_type']