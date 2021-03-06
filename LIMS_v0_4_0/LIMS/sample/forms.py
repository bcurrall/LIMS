from django import forms
from django.forms import modelformset_factory

from LIMS.forms import GenericListFormHelper

from .models import Sample

# General notes
# TODO sytlize filter maybe further to fix conflict between layout and filter parameters (e.g., exact vs. icontains)

def get_model_fields(model):
    return model._meta.fields

class UploadFileForm(forms.Form):
    myfile = forms.FileField()

class SampleForm(forms.ModelForm):

    class Meta:
        model = Sample
        exclude = []
        widgets = {
            'other_genetic_info': forms.Textarea(attrs={'rows': 1, 'cols': 15}),
            'phenotype_desc': forms.Textarea(attrs={'rows': 1, 'cols': 15}),
            'sample_comments': forms.Textarea(attrs={'rows': 1, 'cols': 15}),
            'tracking_comments': forms.Textarea(attrs={'rows': 1, 'cols': 15}),
        }
#
# SampleFormSet = modelformset_factory(Sample, form=SampleForm, fields=('name', 'sample_type', 'conc', 'vol'), extra=1)
#

class SampleListFormHelper(GenericListFormHelper):
    model = Sample
    field_list = ['project_name', 'name', 'sample_type', ]

    def __init__(self):
        self.fields = []
        super().get_layout()
        super().__init__()

class SimpleSampleListFormHelper(SampleListFormHelper):
    field_list_update = []

class TrackingSampleListFormHelper(SampleListFormHelper):
    field_list_update = ['received','stored','active',]

class FreezerSampleListFormHelper(SampleListFormHelper):
    model = Sample
    field_list_update = ['freezer_name']

class FullSampleListFormHelper(SampleListFormHelper):
    model = Sample
    field_list_update = []