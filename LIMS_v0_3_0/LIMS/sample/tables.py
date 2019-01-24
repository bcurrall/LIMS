# tutorial/tables.py
import django_tables2 as tables
from .models import Sample

class SampleTableBasic(tables.Table):

    def __init__(self, fields):
        self.fields = fields


    selection = tables.CheckBoxColumn(
        accessor="pk",
        attrs={"th__input":{"onclick": "toggle(this)"}},
        orderable=False
    )

    class Meta:
        model = Sample
        # add class="paleblue" to <table> tag
        attrs = {'class': 'paleblue'}
        fields = fields

class SampleTableAdvanced(tables.Table):
    selection = tables.CheckBoxColumn(
        accessor="pk",
        attrs={"th__input":{"onclick": "toggle(this)"}},
        orderable=False
    )

    class Meta:
        model = Sample
        # add class="paleblue" to <table> tag
        attrs = {'class': 'paleblue'}
        fields = ('project_name', 'sample_name', 'aliquot_id', 'sample_type', 'conc', 'vol', )
