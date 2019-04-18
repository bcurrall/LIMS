from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views import generic
from django.views.generic import View, DeleteView, CreateView, FormView, ListView
from django.forms import modelformset_factory, formset_factory
from django.urls import reverse_lazy, reverse
from django.views.generic.detail import SingleObjectMixin
from LIMS.views import GenericCreateFormSet
from .models import Sample
from .forms import UploadFileForm, SampleForm, SampleFormSet
from .tables import SampleTableBasic, SampleTableAdvanced, DelSampleTableAdvanced
from .filters import SampleFilter
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django_tables2 import RequestConfig

# for working with excel in exports and imports
import xlwt
import csv

#test imports
from django.contrib.auth.models import User


# TODO archive all def based views
# landing page for samples and browser for sample list
def browser(request):
    title = 'Sample Browser'
    basic_url = 'sample:browser'
    advanced_url = 'sample:browser'

    qset = Sample.objects.all()
    filter = SampleFilter(request.GET, queryset=qset)
    table = SampleTableAdvanced(filter.qs)

    if "basic" in request.POST:
        table = SampleTableBasic(filter.qs)

    if "advanced" in request.POST:
        table = SampleTableAdvanced(filter.qs)

    #TODO add dynamic paginate in terms of number pre page
    table.paginate(page=request.GET.get('page', 1), per_page=15)

    #TODO add delete, edit, archive and process buttons

    context = {
        'button_type': 'buttons_1.html',
        'title': title,
        "basic_url": basic_url,
        "advanced_url": advanced_url,
        "delete_url": 'delete',
        # "formset": formset,
        "table": table,
        # "extras": extras,
        # "upload_form": upload_form,
    }

    return render(request, 'sample/browser.html', context)

# Add sample view - allows users to add new samples to db
def add(request):
    title = 'Enter Basic Samples Information'
    basic_url = 'sample:add'
    advanced_url = 'sample:add'
    extras = 5
    pks = list()
    qset = Sample.objects.none()
    data = ()
    upload_form = UploadFileForm()

    if "quantity" in request.POST:
        extras = int(request.POST['quantity'])

    if "export_btn" in request.POST:
        # from https://simpleisbetterthancomplex.com/tutorial/2016/07/29/how-to-export-to-excel.html
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="samples.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Sample')
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        # TODO make dynamic columns
        columns = ['sample_name', 'sample_type', 'conc', 'vol']
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        wb.save(response)
        return response

    if "upload_btn" in request.POST:
        upload_form = UploadFileForm(request.POST, request.FILES)
        if upload_form.is_valid():
            print("valid")
            filehandle = request.FILES['myfile']
            data = filehandle.get_records()
            for record in data:
                count = count + 1
                sample_name = record['sample_name']
                # TODO figure out how to prevent saving when uploading
                sample_record = Sample.objects.get_or_create(sample_name=sample_name)
                sample = sample_record[0]
                record['sample'] = sample.id
            extras = count


    SampleFormSet = modelformset_factory(Sample, form=SampleForm, extra=extras)
    formset = SampleFormSet(queryset=qset, initial=data)

    table = SampleTableBasic(Sample.objects.all())

    if "save_btn" in request.POST:
        formset = SampleFormSet(request.POST)
        if formset.is_valid():
            record_num = int(0)
            record_add = int(0)
            for form in formset:
                record_num += 1
                if form.is_valid():
                    if form.cleaned_data == {}:
                        messages.warning(request, 'Record #%d did not add because required data was missing.' % record_num)
                    else:
                        record_add += 1
                        form.save()
                else:
                    messages.warning(request, 'Form Error')
            messages.success(request, '%d records added successfully.' % record_add)
        else:
            messages.warning(request, 'Formset Error')

        return HttpResponseRedirect('/sample')

    context = {
        'button_type': 'buttons_1.html',
        'title': title,
        "basic_url": basic_url,
        "advanced_url": advanced_url,
        "formset": formset,
        "table": table,
        "extras": extras,
        "upload_form": upload_form,
    }

    return render(request, 'sample/add.html', context)


### test section
def export_users_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'

    writer = csv.writer(response)
    writer.writerow(['Username', 'First name', 'Last name', 'Email address'])

    users = User.objects.all().values_list('username', 'first_name', 'last_name', 'email')
    for user in users:
        writer.writerow(user)

    return response

def export_users_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['sample_name', 'sample_type', 'conc', 'vol', ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Sample.objects.all().values_list('sample_name', 'sample_type', 'conc', 'vol')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def test(request):
    SampleFormSet = formset_factory(SampleForm, extra=2)

    context = {
        "formset": SampleFormSet(),
    }
    return render(request, 'test.html', context)

def delete(request):
    title = 'Are you sure you want to delete the following samples?'
    pks = request.POST.getlist("selection")
    sample = Sample.objects.filter(pk__in=pks)
    table = SampleTableAdvanced(Sample.objects.filter(pk__in=pks))

    if request.method == "POST":
        if "del_confirm_btn" in request.POST:
            num_deleted = len(pks)
            sample.delete()
            messages.warning(request, '%d samples deleted.' %num_deleted)
            return HttpResponseRedirect('/sample')
        if "no_btn" in request.POST:
            messages.success(request, 'No records were deleted.')
            return HttpResponseRedirect('/sample')

    context = {
        # "add_url": add_url,
        # "select_url": select_url,
        "title": title,
        "table": table,
        # "num_deleted": num_deleted,
    }
    return render(request, 'sample/delete.html', context)

def edit(request):
    title = 'Edit Sample Information'
    subtitle = 'List of samples to edit be generated from sample browser.'
    basic_url = 'sample:edit'
    advanced_url = 'sample:edit'
    extras = 0

    pks = request.POST.getlist("selection")
    qset = Sample.objects.filter(pk__in=pks)

    data = ()
    upload_form = UploadFileForm()

    if "export_btn" in request.POST:
        # from https://simpleisbetterthancomplex.com/tutorial/2016/07/29/how-to-export-to-excel.html
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="samples.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Sample')
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        # TODO make dynamic columns
        columns = ['sample_name', 'sample_type', 'conc', 'vol']
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        wb.save(response)
        return response

    if "upload_btn" in request.POST:
        upload_form = UploadFileForm(request.POST, request.FILES)
        if upload_form.is_valid():
            print("valid")
            filehandle = request.FILES['myfile']
            data = filehandle.get_records()
            count = 0
            for record in data:
                count = count + 1
                sample_name = record['sample_name']
                # TODO figure out how to prevent saving when uploading
                sample_record = Sample.objects.get_or_create(sample_name=sample_name)
                sample = sample_record[0]
                record['sample'] = sample.id
            extras = count


    SampleFormSet = modelformset_factory(Sample, form=SampleForm, extra=extras)
    formset = SampleFormSet(queryset=qset, initial=data)

    table = SampleTableAdvanced(Sample.objects.filter(pk__in=pks))

    if "save_btn" in request.POST:
        formset = SampleFormSet(request.POST)
        if formset.is_valid():
            record_num = int(0)
            record_add = int(0)
            for form in formset:
                record_num += 1
                if form.is_valid():
                    if form.cleaned_data == {}:
                        messages.warning(request, 'Record #%d did not add because required data was missing.' % record_num)
                    else:
                        record_add += 1
                        form.save()
                else:
                    messages.warning(request, 'Form Error')
            messages.success(request, '%d records added successfully.' % record_add)
        else:
            messages.warning(request, 'Formset Error')

        return HttpResponseRedirect('/sample')

    context = {
        'button_type': 'buttons_1.html',
        'title': title,
        'subtitle': subtitle,
        "basic_url": basic_url,
        "advanced_url": advanced_url,
        "formset": formset,
        "table": table,
        "extras": extras,
        "upload_form": upload_form,
    }

    return render(request, 'sample/edit.html', context)

class TestClass(View):
    title = 'Enter Basic Samples Information'
    basic_url = 'sample:add'
    advanced_url = 'sample:add'
    extras = 5
    pks = list()
    qset = Sample.objects.none()
    data = ()
    upload_form = UploadFileForm()

    form_class = SampleForm
    table = SampleTableBasic(Sample.objects.all())
    template_name = 'sample/test.html'

    context = {
        'table': table,
    }

    def get(self, request):
        form = self.form_class(None)
        table = self.table_class
        context = {
            'form': form,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        pass

class DeleteTest(DeleteView):
    model = Sample
    success_url = reverse_lazy('sample:browser')



# TODO make update, delete, detail and list class based formset/form views

### Sample ListViews

class SampleListView(ListView):
    template_name = 'sample/testview.html'
    model = Sample
    title = "Browser"

    qset = Sample.objects.all()
    filter = SampleFilter(queryset=qset)
    table = SampleTableAdvanced(filter.qs)




    def get_context_data(self, *args, **kwargs):  # gets context for building formset
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['table'] = self.table
        RequestConfig(self.request, paginate={'per_page': 15}).configure(self.table)
        # context['button_type'] = self.button_type
        # context['basic_url'] = self.basic_url
        # context['advanced_url'] = self.advanced_url
        # context['buttons'] = self.buttons
        return context




# TODO make all specific inherited class based views in each project

##### Sample CreateViews
# CreateView base (inherits from LIMS Generic CreateView)
class SampleCreateFormSetBase(GenericCreateFormSet):
    template_name = 'sample/create.html'
    success_url = reverse_lazy('sample:browser')
    button_type = 'buttons_1.html'
    basic_url = 'sample:create_basic'
    advanced_url = 'sample:create_full'
    model = Sample
    form_class = SampleForm
    # field = ('project_name','sample_name', 'sample_type')

# CreateViews that inherits from the Base - allows options to restrict fields and stylize buttons
class SampleCreateFormSetBasic(SampleCreateFormSetBase):
    title = 'Enter Samples Information - Basic Information'
    buttons = [
        {"name": 'Basic', "class": 'btn btn-success', "url": 'sample:create_basic'},
        {"name": 'Extract', "class": 'btn btn-default', "url": 'sample:create_extract'},
        {"name": 'Cell Line', "class": 'btn btn-default', "url": 'sample:create_cell'},
        {"name": 'Tissue', "class": 'btn btn-default', "url": 'sample:create_tissue'},
        {"name": 'Full', "class": 'btn btn-default', "url": 'sample:create_full'},
    ]
    field = ('project_name','sample_name', 'aliquot_id', 'sample_type')

class SampleCreateFormSetExtract(SampleCreateFormSetBase):
    title = 'Enter Samples Information - Extract'
    buttons = [
        {"name": 'Basic', "class": 'btn btn-default', "url": 'sample:create_basic'},
        {"name": 'Extract', "class": 'btn btn-success', "url": 'sample:create_extract'},
        {"name": 'Cell Line', "class": 'btn btn-default', "url": 'sample:create_cell'},
        {"name": 'Tissue', "class": 'btn btn-default', "url": 'sample:create_tissue'},
        {"name": 'Full', "class": 'btn btn-default', "url": 'sample:create_full'},
    ]
    field = ('project_name','sample_name','aliquot_id','sample_type','source_tissue','conc','vol', 'conc_nanodrop',
             'conc_tapestation','rin_din_tapestation','conc_qubit','species','gender','family_id','relationship','study_model','case_control','collected_by','date_collected',
             )

class SampleCreateFormSetCellLine(SampleCreateFormSetBase):
    title = 'Enter Samples Information - Full Information'
    buttons = [
        {"name": 'Basic', "class": 'btn btn-default', "url": 'sample:create_basic'},
        {"name": 'Extract', "class": 'btn btn-default', "url": 'sample:create_extract'},
        {"name": 'Cell Line', "class": 'btn btn-success', "url": 'sample:create_cell'},
        {"name": 'Tissue', "class": 'btn btn-default', "url": 'sample:create_tissue'},
        {"name": 'Full', "class": 'btn btn-default', "url": 'sample:create_full'},
    ]
    field = ('project_name','sample_name','aliquot_id','sample_type','source_tissue','conc','vol','weight',
             'cells','alt_name1','alt_name2','conc_nanodrop','conc_tapestation','rin_din_tapestation','conc_qubit',
             'species','gender','family_id','relationship','study_model','case_control','collected_by','date_collected',
             'collection_batch','year_of_birth','race','ethnicity','date_of_birth','strain','brood','cell_line_id',
             'passage_number','cell_line_mutation','cell_line_type','karyotype','genetic_array','other_genetic_info',
             'hpo','phenotype_desc','sample_comments','archived','freezer_name','freezer_type','freezer_shelf',
             'freezer_rack','freezer_row','freezer_column','box_name','box_type','aliquot_pos_row',
             'aliquot_pos_column','received','received_date','active','deactivated_date','deactivated_type',
             'status_comments')

class SampleCreateFormSetTissue(SampleCreateFormSetBase):
    title = 'Enter Samples Information - Human Tissues'
    buttons = [
        {"name": 'Basic', "class": 'btn btn-default', "url": 'sample:create_basic'},
        {"name": 'Extract', "class": 'btn btn-default', "url": 'sample:create_extract'},
        {"name": 'Cell Line', "class": 'btn btn-default', "url": 'sample:create_cell'},
        {"name": 'Tissue', "class": 'btn btn-success', "url": 'sample:create_tissue'},
        {"name": 'Full', "class": 'btn btn-default', "url": 'sample:create_full'},
    ]
    field = ('project_name','sample_name','sample_type','source_tissue','weight',
             'species','gender','family_id','relationship','study_model','case_control','collected_by','date_collected',
             'collection_batch','year_of_birth','race','ethnicity','karyotype','genetic_array','other_genetic_info',
             'hpo','phenotype_desc','sample_comments')

class SampleCreateFormSetFull(SampleCreateFormSetBase):
    title = 'Enter Samples Information - Full Information'
    buttons = [
        {"name": 'Basic', "class": 'btn btn-default', "url": 'sample:create_basic'},
        {"name": 'Extract', "class": 'btn btn-default', "url": 'sample:create_extract'},
        {"name": 'Cell Line', "class": 'btn btn-default', "url": 'sample:create_cell'},
        {"name": 'Tissue', "class": 'btn btn-default', "url": 'sample:create_tissue'},
        {"name": 'Full', "class": 'btn btn-success', "url": 'sample:create_full'},
    ]
    field = ('project_name','sample_name','aliquot_id','sample_type','source_tissue','conc','vol','weight',
             'cells','alt_name1','alt_name2','conc_nanodrop','conc_tapestation','rin_din_tapestation','conc_qubit',
             'species','gender','family_id','relationship','study_model','case_control','collected_by','date_collected',
             'collection_batch','year_of_birth','race','ethnicity','date_of_birth','strain','brood','cell_line_id',
             'passage_number','cell_line_mutation','cell_line_type','karyotype','genetic_array','other_genetic_info',
             'hpo','phenotype_desc','sample_comments','archived','freezer_name','freezer_type','freezer_shelf',
             'freezer_rack','freezer_row','freezer_column','box_name','box_type','aliquot_pos_row',
             'aliquot_pos_column','received','received_date','active','deactivated_date','deactivated_type',
             'status_comments')
