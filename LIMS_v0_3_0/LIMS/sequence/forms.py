from django import forms
from .models import WUSSubmission, WUSPool
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class UploadFileForm(forms.Form):
    myfile = forms.FileField()

class WUSSubmissionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(WUSSubmissionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-2'
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
