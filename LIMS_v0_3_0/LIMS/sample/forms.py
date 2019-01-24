from django import forms
from .models import Sample


class UploadFileForm(forms.Form):
    myfile = forms.FileField()

class SampleForm(forms.ModelForm):
    class Meta:
        model = Sample
        fields = ['sample_name', 'sample_type', 'conc', 'vol']
