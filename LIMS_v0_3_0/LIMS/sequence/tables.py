import django_tables2 as tables
from django_tables2_column_shifter.tables import ColumnShiftTable

from .models import WUSLaneResult, WUSSubmission


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

class WUSLaneResultsTable(ColumnShiftTable):

    selection = tables.CheckBoxColumn(
        accessor="pk",
        attrs={"th__input": {"onclick": "toggle(this)"}},
        orderable=False
    )

    class Meta:
        model = WUSLaneResult
        attrs = {'class': 'paleblue'}
        sequence = ('selection',)

