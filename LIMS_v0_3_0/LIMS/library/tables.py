import django_tables2 as tables
from .models import Library, Pool
from django_tables2_column_shifter.tables import ColumnShiftTable

# setting up table views for samples
# TODO figure out how to pass variable from views to tables to make this more DRY
class LibraryTable(ColumnShiftTable):

    selection = tables.CheckBoxColumn(
        accessor="pk",
        attrs={"th__input": {"onclick": "toggle(this)"}},
        orderable=False
    )

    class Meta:
        model = Library
        attrs = {'class': 'paleblue'}
        sequence = ('selection',)

class PoolTable(ColumnShiftTable):

    selection = tables.CheckBoxColumn(
        accessor="pk",
        attrs={"th__input": {"onclick": "toggle(this)"}},
        orderable=False
    )

    class Meta:
        model = Pool
        attrs = {'class': 'paleblue'}
        sequence = ('selection',)

