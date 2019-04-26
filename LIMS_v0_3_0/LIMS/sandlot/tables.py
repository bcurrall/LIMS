import django_tables2 as tables
from .models import Author
from sample.models import Sample
from django_tables2_column_shifter.tables import ColumnShiftTable

class AuthorTable(tables.Table):
    class Meta:
        model = Author
        attrs = {"class": "paleblue"}
        per_page = 30

class SampleTable(tables.Table):
    class Meta:
        model = Sample
        attrs = {"class": "paleblue"}
        per_page = 30

class SampleTableBasic(ColumnShiftTable):

    selection = tables.CheckBoxColumn(
        accessor="pk",
        attrs={"th__input": {"onclick": "toggle(this)"}},
        orderable=False
    )

    class Meta:
        model = Sample
        per_page = 15
        attrs = {'class': 'paleblue'}
        fields = ('project_name', 'sample_name', 'sample_type')
        sequence = ('selection',)