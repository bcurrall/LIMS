from django import forms
from .models import Library


class UploadFileForm(forms.Form):
    myfile = forms.FileField()

class LibraryPlateForm(forms.ModelForm):
    class Meta:
        model = Library
        exclude = [
            'illumina_barcode_plate', 'barcode_well', 'i7_barcode', 'i5_barcode', 'library_amount',
            'tapestation_size_bp', 'tapestation_conc', 'tapestation_molarity_nM', 'qpcr_conc',
            'qubit_conc',
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

class PoolForm(forms.ModelForm):

    class Meta:
        model = Library
        fields = []