import django_filters as df
from .models import Author

class AuthorListFilter(df.FilterSet):
    class Meta:
        model = Author
        fields = "__all__"

