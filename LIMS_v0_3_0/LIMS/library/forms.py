from django import forms
from .models import Library, Pool, PoolingAmount
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Fieldset, ButtonHolder, Submit, Row, Column


class LibraryListFormHelper(FormHelper):
    model = Library
    form_tag = True
    form_class = 'form-inline'
    field_template = 'bootstrap3/layout/inline_field.html'
    label_class = 'col-xs-1'
    field_class = 'col-xs-4'
    form_id = 'id_filterForm'
    form_method = 'get'
    layout = Layout('gtc_code', 'library_type', ButtonHolder(
        Submit('submit', 'Filter', css_class='button white right')
    ))


class PoolListFormHelper(FormHelper):
    model = Pool
    form_tag = True
    form_class = 'form-inline'
    field_template = 'bootstrap3/layout/inline_field.html'
    label_class = 'col-xs-1'
    field_class = 'col-xs-4'
    form_id = 'id_filterForm'
    form_method = 'get'
    layout = Layout('gtc_code', 'library_type', ButtonHolder(
        Submit('submit', 'Filter', css_class='button white right')
    ))

class PoolingAmountListFormHelper(FormHelper):
    model = PoolingAmount
    form_tag = True
    form_class = 'form-inline'
    field_template = 'bootstrap3/layout/inline_field.html'
    label_class = 'col-xs-1'
    field_class = 'col-xs-4'
    form_id = 'id_filterForm'
    form_method = 'get'
    layout = Layout('pool_name', ButtonHolder(
        Submit('submit', 'Filter', css_class='button white right')
    ))




class UploadFileForm(forms.Form):
    myfile = forms.FileField()

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

class PoolingAmountForm(forms.ModelForm):
    class Meta:
        model = PoolingAmount
        exclude = []

class PoolForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PoolForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit(input_type='submit', value='Update Pool Metrics', css_class='btn btn-light', name='save_form_btn')) #css_class is apending rather than overwritting
        self.helper.layout = Layout(
            'unique_id',
            'name',
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





#
# STATES = (
#     ('', 'Choose...'),
#     ('MG', 'Minas Gerais'),
#     ('SP', 'Sao Paulo'),
#     ('RJ', 'Rio de Janeiro')
# )
#
# class AddressForm(forms.Form):
#     email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
#     password = forms.CharField(widget=forms.PasswordInput())
#     address_1 = forms.CharField(
#         label='Address',
#         widget=forms.TextInput(attrs={'placeholder': '1234 Main St'})
#     )
#     address_2 = forms.CharField(
#         widget=forms.TextInput(attrs={'placeholder': 'Apartment, studio, or floor'})
#     )
#     city = forms.CharField()
#     state = forms.ChoiceField(choices=STATES)
#     zip_code = forms.CharField(label='Zip')
#     check_me_out = forms.BooleanField(required=False)
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.layout = Layout(
#             Row(
#                 Column('email', css_class='form-group col-md-6 mb-0'),
#                 Column('password', css_class='form-group col-md-6 mb-0'),
#                 css_class='form-row'
#             ),
#             'address_1',
#             'address_2',
#             Row(
#                 Column('city', css_class='form-group col-md-6 mb-0'),
#                 Column('state', css_class='form-group col-md-4 mb-0'),
#                 Column('zip_code', css_class='form-group col-md-2 mb-0'),
#                 css_class='form-row'
#             ),
#             'check_me_out',
#             Submit('submit', 'Sign in')
#         )