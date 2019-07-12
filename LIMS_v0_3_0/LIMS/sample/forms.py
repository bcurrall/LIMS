from django import forms
from django.forms import modelformset_factory, formset_factory

from django.urls import reverse
from crispy_forms.bootstrap import Field, InlineRadios, TabHolder, Tab
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Fieldset, ButtonHolder, Submit

from crispy_forms.bootstrap import InlineField

from .models import Sample


class UploadFileForm(forms.Form):
    myfile = forms.FileField()

class SampleForm(forms.ModelForm):

    class Meta:
        model = Sample
        fields = ['id', 'sample_name', 'sample_type', 'conc', 'vol']
        widgets = {
            'other_genetic_info': forms.Textarea(attrs={'rows': 1, 'cols': 15}),
            'phenotype_desc': forms.Textarea(attrs={'rows': 1, 'cols': 15}),
            'sample_comments': forms.Textarea(attrs={'rows': 1, 'cols': 15}),
            'status_comments': forms.Textarea(attrs={'rows': 1, 'cols': 15}),
        }

SampleFormSet = modelformset_factory(Sample, form=SampleForm, fields=('sample_name', 'sample_type', 'conc', 'vol'), extra=1)

# Forms for browser
class SampleListFormHelper(FormHelper):
    model = Sample
    form_tag = True
    form_class = 'form-inline'
    field_template = 'bootstrap3/layout/inline_field.html'
    label_class = 'col-xs-1'
    field_class = 'col-xs-4'
    form_id = 'id_filterForm'
    form_method = 'get'
    layout = Layout('project_name', 'sample_name', 'sample_type', ButtonHolder(
        Submit('submit', 'Filter', css_class='button white right')
    ))

class SampleListFreezerFormHelper(FormHelper):
    model = Sample
    form_tag = True
    form_class = 'form-inline'
    field_template = 'bootstrap4/layout/inline_field.html'
    label_class = 'col-xs-1'
    field_class = 'col-xs-4'
    form_id = 'id_filterForm'
    form_method = 'get'
    layout = Layout('project_name', 'sample_name', 'sample_type', 'freezer', ButtonHolder(
        Submit('submit', 'Filter', css_class='button white right')
    ))