
print("test")

# tutorial/tables.py
import django_tables2 as tables
from .models import Individual, Sample

class IndividualTable(tables.Table):
    class Meta:
        model = Individual
        # add class="paleblue" to <table> tag
        attrs = {'class': 'paleblue'}

class SampleTable(tables.Table):
    selection = tables.CheckBoxColumn(
        accessor="pk",
        attrs={"th__input":{"onclick": "toggle(this)"}},
        orderable=False
    )

    class Meta:
        model = Sample
        # add class="paleblue" to <table> tag
        attrs = {'class': 'paleblue'}