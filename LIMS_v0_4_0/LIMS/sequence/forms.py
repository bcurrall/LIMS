from django import forms
from .models import WUSSubmission, WUSPool, WUSResult
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Fieldset, ButtonHolder, Submit, Row, Column

from LIMS.forms import GenericListFormHelper

#### Forms


#### FormHelpers
### WUSSubmissions
## Base
class WUSSubmissionListFormHelper(GenericListFormHelper):
    model = WUSSubmission
    field_list = ['batch_id','broad_id']

    def __init__(self):
        self.fields = []
        super().get_layout()
        super().__init__()

### WUSPool
## Base
class WUSPoolListFormHelper(GenericListFormHelper):
    model = WUSPool
    field_list = ['parent_name', 'related_name']

    def __init__(self):
        self.fields = []
        super().get_layout()
        super().__init__()

### WUSResults
## Base
class WUSResultListFormHelper(GenericListFormHelper):
    model = WUSResult
    field_list = ['parent_name', 'related_name', 'broad_id']

    def __init__(self):
        self.fields = []
        super().get_layout()
        super().__init__()





class WUSSubmissionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(WUSSubmissionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit(input_type='submit', value='Update WUS Metrics', css_class='btn btn-light',
                                     name='save_form_btn'))  # css_class is apending rather than overwritting

        # self.helper.form_class = 'form-horizontal'
        # self.helper.label_class = 'col-lg-2'
        # self.helper.field_class = 'col-lg-2'
        # self.helper.field_template = 'bootstrap4/layout/inline_field.html'

        # self.helper.layout = Layout(
        #     'pool_name',
        #     Row(
        #         Column('tapestation_size_bp', css_class='form-group col-md-4 mb-0'),
        #         Column('tapestation_conc', css_class='form-group col-md-4 mb-0'),
        #         Column('tapestation_molarity_nM', css_class='form-group col-md-4 mb-0'),
        #         css_class='form-row',
        #     ),
        #     Row(
        #         Column('qpcr_conc', css_class='form-group col-md-3 mb-0'),
        #         Column('qubit_conc', css_class='form-group col-md-3 mb-0'),
        #         Column('made_date', css_class='form-group col-md-3 mb-0'),
        #         Column('made_by', css_class='form-group col-md-3 mb-0'),
        #         css_class='form-row'
        #     ),
        #     'pool_comments',
        # )

    class Meta:
        model = WUSSubmission
        exclude = []

class WUSPoolForm(forms.ModelForm):

    class Meta:
        model = WUSPool
        exclude = []

class WUSResultForm(forms.ModelForm):
    class Meta:
        model = WUSResult
        exclude = []

#### Other Forms
class UploadFileForm(forms.Form):
    myfile = forms.FileField()

#### Archive
'''
class WUSSubmissionListFormHelper(FormHelper):
    model = WUSSubmission
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
    

class WUSPoolListFormHelper(FormHelper):
    model = WUSPool
    form_tag = True
    form_class = 'form-inline'
    field_template = 'bootstrap3/layout/inline_field.html'
    label_class = 'col-xs-1'
    field_class = 'col-xs-4'
    form_id = 'id_filterForm'
    form_method = 'get'
    layout = Layout('parent_name', 'related_name', ButtonHolder(
        Submit('submit', 'Filter', css_class='button white right')
    ))

class WUSResultListFormHelper(FormHelper):
    model = WUSResult
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

'''

