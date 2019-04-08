from django import forms
from django.forms import modelformset_factory, formset_factory

from .models import Sample


class UploadFileForm(forms.Form):
    myfile = forms.FileField()

class SampleForm(forms.ModelForm):

    class Meta:
        model = Sample
        fields = ['sample_name', 'sample_type', 'conc', 'vol']

SampleFormSet = modelformset_factory(Sample, form=SampleForm, fields=('sample_name', 'sample_type', 'conc', 'vol'), extra=1)