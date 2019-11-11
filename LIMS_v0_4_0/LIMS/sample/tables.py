import django_tables2 as tables
from .models import Sample
from django_tables2_column_shifter.tables import ColumnShiftTable

### setting up table views for PagedFilteredTableView
class SampleTableGeneric(ColumnShiftTable):
    """
    Makes Generic ColumnShiftTable (i.e., the visible column dropdown that allows selection of different columns),
    adds selection box and stylizes the table
    ColumnShiftTable is from package: https://pypi.org/project/django-tables2-column-shifter/
    """
    selection = tables.CheckBoxColumn(
        accessor="pk",
        attrs={"th__input": {"onclick": "toggle(this)"}},
        orderable=False
    )

    class Meta:
        model = Sample
        attrs = {'class': 'paleblue'}
        fields = ('unique_id',)
        sequence = ('selection',)

### instances of SampleTableGeneric with different fields
class SampleTableSimple(SampleTableGeneric):
    class Meta(SampleTableGeneric.Meta):
        fields = ('project_name', 'name', 'sample_type')

class SampleTableTracking(SampleTableGeneric):
    class Meta(SampleTableGeneric.Meta):
        fields = ('project_name', 'name', 'sample_type', 'received', 'received_date', 'stored', 'active',
                  'deactivated_type', 'tracking_comments',)

class SampleTableFreezer(SampleTableGeneric):
    class Meta(SampleTableGeneric.Meta):
        fields = ('project_name', 'name', 'sample_type', 'received','active', 'stored',
                  'freezer_name', 'freezer_type', 'freezer_shelf','freezer_rack','rack_row','rack_column',
                  'box_name','aliquot_pos_row','aliquot_pos_column',)

class SampleTableFull2(SampleTableGeneric):
    class Meta(SampleTableGeneric.Meta):
        model = Sample
        field_get = [f.name for f in model._meta.fields]
        fields = field_get

# class SampleTableFull(SampleTableGeneric):
#     class Meta(SampleTableGeneric.Meta):
#         fields = ('project_name', 'name', 'sample_type')


#test