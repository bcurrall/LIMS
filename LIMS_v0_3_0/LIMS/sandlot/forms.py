from django import forms
from .models import Author
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit

class AuthorListFormHelper(FormHelper):
    model = Author
    form_tag = True
    form_class = 'form-horizontal'
    # helper.label_class = 'col-xs-1'
    # helper.field_class = 'col-xs-4'
    layout = Layout('name', ButtonHolder(
        Submit('submit', 'Filter', css_class='button white right')
    ))