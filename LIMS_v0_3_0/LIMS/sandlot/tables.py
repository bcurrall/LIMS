import django_tables2 as dt2
from .models import Author

class AuthorTable(dt2.Table):
    class Meta:
        model = Author
        attrs = {"class": "paleblue"}
        per_page = 30