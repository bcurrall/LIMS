import django_filters
from django_filters import rest_framework as filters
from .models import WUSSubmission, WUSPool, WUSResult



class WUSSubmissionListFilter(filters.FilterSet):
    class Meta:
        model = WUSSubmission
        fields = "__all__"

class WUSPoolListFilter(filters.FilterSet):
    class Meta:
        model = WUSPool
        fields = "__all__"


class WUSSubmissionFilter(filters.FilterSet):

    class Meta:
        model = WUSSubmission
        fields = []


class WUSResultFilter(filters.FilterSet):

    class Meta:
        model = WUSResult
        fields = []

