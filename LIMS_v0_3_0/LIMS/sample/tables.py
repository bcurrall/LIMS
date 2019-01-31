import django_tables2 as tables
from .models import Sample, var3
from django_tables2_column_shifter.tables import ColumnShiftTable

# setting up table views for samples
# TODO figure out how to pass variable from views to tables to make this more DRY
class SampleTableBasic(ColumnShiftTable):

    selection = tables.CheckBoxColumn(
        accessor="pk",
        attrs={"th__input": {"onclick": "toggle(this)"}},
        orderable=False
    )

    class Meta:
        model = Sample
        attrs = {'class': 'paleblue'}
        fields = ('sample_name',)
        sequence = ('selection',)


class SampleTableAdvanced(ColumnShiftTable):

    selection = tables.CheckBoxColumn(
        accessor="pk",
        attrs={"th__input": {"onclick": "toggle(this)"}},
        orderable=False
    )

    class Meta:
        model = Sample
        attrs = {'class': 'paleblue'}
        sequence = ('selection',)

class DelSampleTableAdvanced(ColumnShiftTable):
    class Meta:
        model = Sample
        attrs = {'class': 'paleblue'}