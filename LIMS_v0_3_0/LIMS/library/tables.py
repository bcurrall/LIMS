import django_tables2 as tables
from .models import Library, Pool, PoolingAmount
from django_tables2_column_shifter.tables import ColumnShiftTable

# setting up table views for samples
# TODO figure out how to pass variable from views to tables to make this more DRY

class LibraryTableSimple(ColumnShiftTable):

    selection = tables.CheckBoxColumn(
        accessor="pk",
        attrs={"th__input": {"onclick": "toggle(this)"}},
        orderable=False
    )

    class Meta:
        model = Library
        attrs = {'class': 'paleblue'}
        fields = ('unique_id', 'gtc_code', 'library_type', 'plate_name', 'well', 'parent_name', 'name',)
        sequence = ('selection',)

class LibraryTableDelete(ColumnShiftTable):

    selection = tables.CheckBoxColumn(
        accessor="pk",
        attrs={"th__input": {"onclick": "toggle(this)"}},
        orderable=False
    )

    class Meta:
        model = Library
        attrs = {'class': 'paleblue'}
        fields = ('unique_id', 'gtc_code', 'library_type', 'plate_name', 'well', 'parent_name', 'name',)
        sequence = ('selection',)

class LibraryTablePlateSetup(ColumnShiftTable):

    selection = tables.CheckBoxColumn(
        accessor="pk",
        attrs={"th__input": {"onclick": "toggle(this)"}},
        orderable=False
    )

    class Meta:
        model = Library
        attrs = {'class': 'paleblue'}
        fields = ('unique_id', 'gtc_code', 'library_type', 'plate_name', 'well', 'parent_name', 'name',
                  'amount_of_sample_used', 'amount_of_water_used', 'plate_comments')
        sequence = ('selection',)

class LibraryTableQC(ColumnShiftTable):

    selection = tables.CheckBoxColumn(
        accessor="pk",
        attrs={"th__input": {"onclick": "toggle(this)"}},
        orderable=False
    )

    class Meta:
        model = Library
        attrs = {'class': 'paleblue'}
        fields = ('unique_id', 'gtc_code', 'library_type', 'plate_name', 'well', 'parent_name', 'name',
                  'illumina_barcode_plate', 'barcode_well', 'i7_barcode', 'i5_barcode', 'library_amount',
                  'tapestation_size_bp', 'tapestation_conc_ng_uL', 'tapestation_molarity_nM', 'qpcr_conc_molarity_nM', 'qubit_conc_ng_uL',
                  )
        sequence = ('selection',)

class LibraryTableFull(ColumnShiftTable):

    selection = tables.CheckBoxColumn(
        accessor="pk",
        attrs={"th__input": {"onclick": "toggle(this)"}},
        orderable=False
    )

    class Meta:
        model = Library
        attrs = {'class': 'paleblue'}
        sequence = ('selection',)

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

class PoolingAmountTable(ColumnShiftTable):

    selection = tables.CheckBoxColumn(
        accessor="pk",
        attrs={"th__input": {"onclick": "toggle(this)"}},
        orderable=False
    )

    class Meta:
        model = PoolingAmount
        attrs = {'class': 'paleblue'}
        sequence = ('selection',)