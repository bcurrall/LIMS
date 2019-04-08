from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views import generic
from django.views.generic import View, DeleteView, CreateView, FormView
from django.forms import modelformset_factory, formset_factory
from django.urls import reverse_lazy, reverse
from django.views.generic.detail import SingleObjectMixin
from .models import Sample
from .forms import UploadFileForm, SampleForm, SampleFormSet
from .tables import SampleTableBasic, SampleTableAdvanced, DelSampleTableAdvanced
from .filters import SampleFilter
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

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

class SampleCreateTest(FormView):
    template_name = 'sample/form.html'
    form_class = SampleForm
    success_url = reverse_lazy('sample:create')

    def get_context_data(self, **kwargs):
        context = super(SampleCreateFormSetTest, self).get_context_data(**kwargs)
        context['formset'] = SampleFormSet(queryset=Sample.objects.none())
        return context


    def get_success_message(self, cleaned_data):
        print("================================")
        print(cleaned_data)
        return "Success"

    # queryset = Sample.objects.all()

    # def form_valid(self, form):
    #     print(form.cleaned_data)
    #     return super().form_valid(form)




# TODO make update, delete, detail and list class based formset/form views
# TODO move generic class based views to generic folder
class CreateFormSet(CreateView):
    # required variables
    # TODO make required variables part of init and/or args
    template_name = 'sample/create.html'
    success_url = reverse_lazy('sample:browser')
    button_type = 'buttons_1.html'
    title = 'Enter Samples Information - Generic Form Class Test'
    basic_url = 'sample:createformsettest'
    advanced_url = 'sample:add'
    model = Sample
    form_class = SampleForm
    field = ('sample_name', 'sample_type', 'conc', 'vol')

    # class global variables
    queryset = model.objects.none()
    initial_data = []
    extra = 1
    upload_form = UploadFileForm()

    def get_formset(self): #makes formset for various defs within class
        formset = modelformset_factory(
            self.model,
            form=self.form_class,
            fields=self.field,
            extra=self.extra
        )
        return formset

    def get_context_data(self, *args, **kwargs): #gets context for building formset
        context = super(CreateFormSet, self).get_context_data(**kwargs)
        formset = self.get_formset()
        context['formset'] = formset(queryset=self.queryset, initial=self.initial_data)
        context['title'] = self.title
        context['button_type'] = self.button_type
        context['basic_url'] = self.basic_url
        print("=========context = ", context)
        return context

    def post(self, request, *args, **kwargs): #handles all posts

        # updates number of records to be handled for "Update" button
        if "quantity" in self.request.POST:
            self.object = None
            print("self.request.POST = ", self.request.POST['quantity'])
            if self.request.POST['quantity'] == "":
                extra = 1
            else:
                extra = int(self.request.POST['quantity'])
            self.extra = extra
            context = self.get_context_data()
            return render(request, self.template_name, context=context)

        # exports file based on formset through "Export" button
        if "export_btn" in request.POST:
            # from https://simpleisbetterthancomplex.com/tutorial/2016/07/29/how-to-export-to-excel.html
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="samples.xls"'
            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Sample')
            row_num = 0
            font_style = xlwt.XFStyle()
            font_style.font.bold = True
            columns = self.field
            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)
            wb.save(response)
            return response

        # uploads form and handles errors through "Choose File" and "Upload" button
        if "upload_btn" in request.POST:
            upload_form = UploadFileForm(request.POST, request.FILES)
            if upload_form.is_valid():
                filehandle = request.FILES['myfile']
                initial_data = filehandle.get_records()
                self.initial_data = initial_data
                self.object = None
                extra = 0
                for record in initial_data:
                    #TODO need to do form validation and/or error reporting associated with uploaded form
                    extra = extra + 1
                self.extra = extra
                context = self.get_context_data()
                return render(request, self.template_name, context=context)
            # TODO unhandled exception form_invalid

        if "save_btn" in self.request.POST:
            formset = self.get_formset()
            formset = formset(request.POST)
            if formset.is_valid():
                print("formset = ", formset)
                record_num = int(0)
                record_add = int(0)
                for form in formset:
                    record_num += 1
                    #TODO need to make validation more DRY - move to seperate def
                    #TODO need to prevent duplicate records and ensure unique naming system
                    if form.is_valid():
                        if form.cleaned_data == {}:
                            messages.warning(request,
                                             'Record #%d did not add because required data was missing.' % record_num)
                        else:
                            record_add += 1
                            form.save()
                    else:
                        messages.warning(request, 'Form Error')
                messages.success(request, '%d records added successfully.' % record_add)
                return HttpResponseRedirect(self.success_url)
            else:
                messages.warning(request, 'Formset Error')
                return self.render_to_response(self.get_context_data(formset=formset))


# TODO make all specific inherited class based views in each project
class SampleCreateFormSet(CreateFormSet):
    template_name = 'sample/create.html'
    success_url = reverse_lazy('sample:browser')
    button_type = 'buttons_1.html'
    title = 'Enter Samples Information - Generic Form Class Test'
    basic_url = 'sample:createformsettest'
    advanced_url = 'sample:add'
    model = Sample
    form_class = SampleForm
    field = ('project_name','sample_name', 'sample_type', 'conc', 'vol','conc_nanodrop')