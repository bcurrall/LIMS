from django import forms
from django.forms import modelformset_factory

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Fieldset, ButtonHolder, Submit

from .models import Sample

# General notes
# TODO sytlize filter maybe further to fix conflict between layout and filter parameters (e.g., exact vs. icontains)

class UploadFileForm(forms.Form):
    myfile = forms.FileField()

class SampleForm(forms.ModelForm):

    class Meta:
        model = Sample
        fields = ['id', 'name', 'sample_type', 'conc', 'vol']
        widgets = {
            'other_genetic_info': forms.Textarea(attrs={'rows': 1, 'cols': 15}),
            'phenotype_desc': forms.Textarea(attrs={'rows': 1, 'cols': 15}),
            'sample_comments': forms.Textarea(attrs={'rows': 1, 'cols': 15}),
            'tracking_comments': forms.Textarea(attrs={'rows': 1, 'cols': 15}),
        }

SampleFormSet = modelformset_factory(Sample, form=SampleForm, fields=('name', 'sample_type', 'conc', 'vol'), extra=1)

# Forms for browser
class GenericListFormHelper(FormHelper):
    model = Sample
    form_tag = True
    form_class = 'form-inline'
    field_template = 'bootstrap3/layout/inline_field.html'
    label_class = 'col-xs-1'
    field_class = 'col-xs-4'
    form_id = 'id_filterForm'
    form_method = 'get'
    # layout = Layout('project_name', 'name', 'sample_type', ButtonHolder(
    #     Submit('submit', 'Filter', css_class='button white right')
    # ))

class SampleListFormHelper(GenericListFormHelper):
    layout = Layout('project_name', 'name', 'sample_type', ButtonHolder(
        Submit('submit', 'Filter', css_class='button white right')
    ))

class SampleListFreezerFormHelper(GenericListFormHelper):
    layout = Layout('project_name', 'name', 'sample_type', 'freezer_name', ButtonHolder(
        Submit('submit', 'Filter', css_class='button white right')
    ))