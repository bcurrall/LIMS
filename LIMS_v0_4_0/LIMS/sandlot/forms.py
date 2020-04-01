from django import forms
from .models import Author, Thread, Post
from sample.models import Sample
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit

class AuthorListFormHelper(FormHelper):
    model = Author
    form_tag = True
    form_class = 'form-horizontal'
    label_class = 'col-xs-1'
    field_class = 'col-xs-4'
    layout = Layout('name', ButtonHolder(
        Submit('submit', 'Filter', css_class='button white right')
    ))

class SampleListFormHelper(FormHelper):
    model = Sample
    form_tag = True
    form_class = 'form-inline'
    label_class = 'col-xs-1'
    field_class = 'col-xs-4'
    form_id = 'id_filterForm'
    form_method = 'get'
    layout = Layout('project_name', 'sample_name', 'sample_type', ButtonHolder(
        Submit('submit', 'Filter', css_class='button white right')
    ))

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('content',)

class ThreadFrom(forms.ModelForm):
    class Meta:
        model = Thread
        exclude = []
