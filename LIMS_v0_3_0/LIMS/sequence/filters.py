import django_filters
from django_filters import rest_framework as filters
from .models import WUSSubmission, WUSLaneResult



class WUSSubmissionFilter(filters.FilterSet):

    class Meta:
        model = WUSSubmission
        fields = []


class WUSLaneResultFilter(filters.FilterSet):

    class Meta:
        model = WUSLaneResult
        fields = []

