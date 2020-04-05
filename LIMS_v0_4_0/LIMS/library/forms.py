from django import forms
from .models import Library, Pool, PoolingAmount
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Fieldset, ButtonHolder, Submit, Row, Column

from LIMS.forms import GenericListFormHelper

#### Forms

class LibraryForm(forms.ModelForm):
    class Meta:
        model = Library
        exclude = []
        widgets = {
            'plate_comments': forms.Textarea(attrs={'rows': 1, 'cols': 15}),
            'qc_comments': forms.Textarea(attrs={'rows': 1, 'cols': 15}),
        }

class LibraryPlateForm(forms.ModelForm):
    class Meta:
        model = Library
        exclude = [
            'illumina_barcode_plate', 'barcode_well', 'i7_barcode', 'i5_barcode', 'library_amount',
            'tapestation_size_bp', 'tapestation_conc', 'tapestation_molarity_nM', 'qpcr_conc',
            'qubit_conc', 'qc_comments',
        ]
        widgets = {
            'plate_comments': forms.Textarea(attrs={'rows': 1, 'cols': 15}),
        }

class LibraryValidateForm(forms.ModelForm):
    class Meta:
        model = Library
        exclude = [
            'gtc_code', 'amount_of_sample_used', 'amount_of_water_used', 'plate_comments',
        ]
        widgets = {
            'qc_comments': forms.Textarea(attrs={'rows': 1, 'cols': 15}),
        }

class PoolForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PoolForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit(input_type='submit', value='Update Pool Metrics', css_class='btn btn-light', name='save_form_btn')) #css_class is apending rather than overwritting
        self.helper.layout = Layout(
            'unique_id',
            # 'name',
            'batch_id',
            Row(
                Column('tapestation_size_bp', css_class='form-group col-md-4 mb-0'),
                Column('tapestation_conc', css_class='form-group col-md-4 mb-0'),
                Column('tapestation_molarity_nM', css_class='form-group col-md-4 mb-0'),
                css_class='form-row',
            ),
            Row(
                Column('qpcr_conc', css_class='form-group col-md-3 mb-0'),
                Column('qubit_conc', css_class='form-group col-md-3 mb-0'),
                Column('made_date', css_class='form-group col-md-3 mb-0'),
                Column('made_by', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            'pool_comments',
        )

    class Meta:
        model = Pool
        exclude = []
        widgets = {
            'pool_comments': forms.Textarea(attrs={'rows': 1, 'cols': 15}),
        }

class PoolingAmountForm(forms.ModelForm):

    class Meta:
        model = PoolingAmount
        exclude = []

#### FormHelpers
### Libraries
##Base
class LibraryListFormHelper(GenericListFormHelper):
    model = Library
    field_list = ['gtc_code', 'batch_id', 'library_type',]

    def __init__(self):
        self.fields = []
        super().get_layout()
        super().__init__()

### Pools
## Base
class PoolListFormHelper(GenericListFormHelper):
    model = Pool
    field_list = ['batch_id']

    def __init__(self):
        self.fields = []
        super().get_layout()
        super().__init__()

### Pooling amounts
## Base
class PoolingAmountListFormHelper(GenericListFormHelper):
    model = Pool
    field_list = ['parent_name',]

    def __init__(self):
        self.fields = []
        super().get_layout()
        super().__init__()

### Other forms
class UploadFileForm(forms.Form):
    myfile = forms.FileField()

##Archive
'''

#
# class LibraryListFormHelper(FormHelper):
#     model = Library
#     form_tag = True
#     form_class = 'form-inline'
#     field_template = 'bootstrap3/layout/inline_field.html'
#     label_class = 'col-xs-1'
#     field_class = 'col-xs-4'
#     form_id = 'id_filterForm'
#     form_method = 'get'
#     layout = Layout('gtc_code', 'batch_id', 'library_type', ButtonHolder(
#         Submit('submit', 'Filter', css_class='button white right')
#     ))



# class PoolListFormHelper(FormHelper):
#     model = Pool
#     form_tag = True
#     form_class = 'form-inline'
#     field_template = 'bootstrap3/layout/inline_field.html'
#     label_class = 'col-xs-1'
#     field_class = 'col-xs-4'
#     form_id = 'id_filterForm'
#     form_method = 'get'
#     layout = Layout('gtc_code', 'library_type', ButtonHolder(
#         Submit('submit', 'Filter', css_class='button white right')
#     ))


#
# class PoolingAmountListFormHelper(FormHelper):
#     model = PoolingAmount
#     form_tag = True
#     form_class = 'form-inline'
#     field_template = 'bootstrap3/layout/inline_field.html'
#     label_class = 'col-xs-1'
#     field_class = 'col-xs-4'
#     form_id = 'id_filterForm'
#     form_method = 'get'
#     layout = Layout('parent_name', ButtonHolder(
#         Submit('submit', 'Filter', css_class='button white right')
#     ))
#
'''