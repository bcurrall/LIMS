from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Fieldset, ButtonHolder, Submit, HTML, BaseInput, Row

class UploadFileForm(forms.Form):
    myfile = forms.FileField()

class GenericListFormHelper(FormHelper):
    """
    FormHelper for creating search buttons used in conjuction with browser
    https://django-crispy-forms.readthedocs.io/en/latest/crispy_tag_forms.html#bootstrap3-inline-forms
    """

    model = None
    form_tag = True
    form_class = 'form-inline'
    field_template = 'bootstrap3/layout/inline_field.html'
    label_class = 'col-xs-1'
    field_class = 'col-xs-4'
    form_id = 'id_filterForm'
    form_method = 'get'
    render_unmentioned_fields = False
    field_list = ['project_name', 'name', 'sample_type', ]
    field_list_update = []

    def get_layout(self):
        print('===============get_layout=================')
        fields = self.field_list + self.field_list_update
        self.layout = Layout(Row(*fields, style='margin:10px 0px'),
                        Row(HTML('''
                                        <label for='perpage'>Per Page</label>
                                        <input id="perpage" name="per_page" value="{{ extras }}">
                                    '''
                                 ),
                            style='margin:10px 0px'
                            ),
                        ButtonHolder(
                            Submit('submit', 'Filter', css_class='button white right')
                        )
                        )