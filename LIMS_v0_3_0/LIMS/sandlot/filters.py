import django_filters as df
from .models import Author
from sample.models import Sample

class AuthorListFilter(df.FilterSet):
    class Meta:
        model = Author
        fields = "__all__"

class SampleListFilter(df.FilterSet):
    class Meta:
        model = Sample
        fields = "__all__"
