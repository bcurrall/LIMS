from django import forms
from django.forms import formset_factory, BaseFormSet, inlineformset_factory, BaseInlineFormSet
from .models import Individual, Sample, Sample2, Freezer, Box
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from betterforms.multiform import MultiModelForm
import os



### new forms 01_10_19

class SampleFormHuman(forms.ModelForm):
    class Meta:
        model = Sample2
        exclude = []

class SampleMultiFormHuman(forms.ModelForm):
    class Meta:
        model = Sample2
        exclude = []

class SampleForm2(forms.ModelForm):
    class Meta:
        model = Sample2
        fields = ['sample_name', 'sample_type', 'source_tissue', 'conc', 'vol', 'alt_name1']

### old forms prior to 01_10_19

class UploadFileForm(forms.Form):
    myfile = forms.FileField()


class SampleForm(forms.ModelForm):
    class Meta:
        model = Sample
        fields = ['individual', 'sample_name', 'type', 'o_tissue', 'conc', 'vol']

class SampleFormSm(forms.ModelForm):
    class Meta:
        model = Sample
        fields = ['individual', 'sample_name', 'type']

class SampleMultiForm(forms.ModelForm):
    class Meta:
        model = Sample
        exclude = ['individual', 'active']


class IndividualForm(forms.ModelForm):
    class Meta:
        model = Individual
        fields = ['name', 'alt_name1', 'project', 'species', 'family_id',
                  'relationship', 'karyotype', 'other_genetic_info', 'gender', 'year_of_birth']


class FullSampleForm(forms.ModelForm):
    name = forms.CharField(label='Name', required=True)
    alt_name1 = forms.CharField(label='Alt Name', required=False)
    project = forms.CharField(label='Project', required=False)
    species = forms.CharField(label='Species', required=False)
    family_id = forms.CharField(label='Family ID', required=False)
    relationship = forms.CharField(label='Relationship', required=False)
    karyotype = forms.CharField(label='Karyotype', required=False)
    other_genetic_info = forms.CharField(label='Other Genetic Info', required=False)
    gender = forms.CharField(label='Gender', required=False)
    year_of_birth = forms.IntegerField(required=False)

    class Meta:
        model = Sample
        exclude = ['individual', 'active']


class FreezerForm(forms.ModelForm):
    class Meta:
        model = Freezer
        fields = ['name', 'freezer_type', 'shelves', 'racks', 'rows', 'columns']


class BoxForm(forms.ModelForm):
    class Meta:
        model = Box
        fields = ['name','freezer_pos', 'box_type', 'rows', 'columns']

