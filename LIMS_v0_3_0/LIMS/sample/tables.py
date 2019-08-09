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
        fields = ('project_name', 'unique_id', 'name', 'sample_type')
        sequence = ('selection',)

class SampleTableTracking(ColumnShiftTable):

    selection = tables.CheckBoxColumn(
        accessor="pk",
        attrs={"th__input": {"onclick": "toggle(this)"}},
        orderable=False
    )

    class Meta:
        model = Sample
        attrs = {'class': 'paleblue'}
        fields = ('project_name', 'unique_id', 'name', 'sample_type',
                  'received', 'received_date', 'stored', 'active', 'deactivated_type', 'tracking_comments')
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
        fields = ('project_name', 'unique_id', 'name', 'sample_type', 'received','active', 'stored',
                  'freezer_name', 'freezer_type', 'freezer_shelf','freezer_rack','rack_row','rack_column',
                  'box_name','aliquot_pos_row','aliquot_pos_column'
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