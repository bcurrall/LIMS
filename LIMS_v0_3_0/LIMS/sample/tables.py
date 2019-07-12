import django_tables2 as tables
from .models import Sample
from django_tables2_column_shifter.tables import ColumnShiftTable

# setting up table views for samples
# TODO figure out how to pass variable from views to tables to make this more DRY
class SampleTableSimple(ColumnShiftTable):

    selection = tables.CheckBoxColumn(
        accessor="pk",
        attrs={"th__input": {"onclick": "toggle(this)"}},
        orderable=False
    )

    class Meta:
        model = Sample
        attrs = {'class': 'paleblue'}
        fields = ('project_name', 'sample_name', 'sample_type')
        sequence = ('selection',)

class SampleTableFreezer(ColumnShiftTable):

    selection = tables.CheckBoxColumn(
        accessor="pk",
        attrs={"th__input": {"onclick": "toggle(this)"}},
        orderable=False
    )

    class Meta:
        model = Sample
        attrs = {'class': 'paleblue'}
        sequence = ('selection',)
        fields = ('project_name', 'sample_name', 'sample_type', 'received ', 'received_date','archived','freezer_name',
                  'freezer_type', 'freezer_shelf','freezer_rack','freezer_row','freezer_column','box_name','box_type',
                  'aliquot_pos_row','aliquot_pos_column','aliquot_pos_column', 'active', 'deactivated_date', 'deactivated_type',
                  'status_comments'
                  )

class DelSampleTableAdvanced(ColumnShiftTable):
    class Meta:
        model = Sample
        attrs = {'class': 'paleblue'}

class SampleTableFull(ColumnShiftTable):

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