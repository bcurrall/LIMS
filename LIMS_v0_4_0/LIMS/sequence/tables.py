import django_tables2 as tables
from django_tables2_column_shifter.tables import ColumnShiftTable

from .models import WUSResult, WUSSubmission, WUSPool


# setting up table views for samples
# TODO figure out how to pass variable from views to tables to make this more DRY
class WUSSubmissionTable(ColumnShiftTable):

    selection = tables.CheckBoxColumn(
        accessor="pk",
        attrs={"th__input": {"onclick": "toggle(this)"}},
        orderable=False
    )

    class Meta:
        model = WUSSubmission
        attrs = {'class': 'paleblue'}
        sequence = ('selection',)


class WUSPoolTable(ColumnShiftTable):

    selection = tables.CheckBoxColumn(
        accessor="pk",
        attrs={"th__input": {"onclick": "toggle(this)"}},
        orderable=False
    )

    class Meta:
        model = WUSPool
        attrs = {'class': 'paleblue'}
        sequence = ('selection',)


class WUSResultsTable(ColumnShiftTable):

    selection = tables.CheckBoxColumn(
        accessor="pk",
        attrs={"th__input": {"onclick": "toggle(this)"}},
        orderable=False
    )

    class Meta:
        model = WUSResult
        attrs = {'class': 'paleblue'}
        sequence = ('selection',)

