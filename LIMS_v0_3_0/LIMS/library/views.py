from django.shortcuts import render
from django.forms import modelformset_factory, formset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse_lazy
from LIMS.views import GenericUpdateFormSet, PagedFilteredTableView
from .models import Library, Pool, PoolingAmount
from .forms import UploadFileForm, LibraryPlateForm, LibraryValidateForm, PoolForm, PoolingAmountForm, LibraryForm, LibraryListFormHelper, PoolListFormHelper, PoolingAmountListFormHelper
from .tables import LibraryTableSimple, LibraryTableDelete, LibraryTablePlateSetup, LibraryTableQC, LibraryTable, LibraryTableFull, PoolTable, PoolingAmountTable
from .filters import LibraryListFilter, LibraryFilter, PoolListFilter, PoolFilter, PoolingAmountListFilter

from sample.models import Sample
from sample.forms import SampleForm, SampleListFormHelper
from sample.filters import SampleListFilter
from sample.views import SampleTableListBase
from sample.tables import SampleTableSimple

import datetime

# for working with excel in exports and imports
import xlwt
import csv


# time stamp
now = datetime.datetime.now()
date_stamp = now.strftime("%d%m%Y")



def delete_pool(request):
    title = 'Are you sure you want to delete the following libraries?'
    pks = request.POST.getlist("selection")
    library = Pool.objects.filter(pk__in=pks)
    table = PoolTable(Pool.objects.filter(pk__in=pks))

    if request.method == "POST":
        if "del_confirm_btn" in request.POST:
            num_deleted = len(pks)
            library.delete()
            messages.warning(request, '%d libraries deleted.' %num_deleted)
            return HttpResponseRedirect('/library')
        if "no_btn" in request.POST:
            messages.success(request, 'No libraries were deleted.')
            return HttpResponseRedirect('/library')

    context = {
        # "add_url": add_url,
        # "select_url": select_url,
        "title": title,
        "table": table,
        # "num_deleted": num_deleted,
    }
    return render(request, 'library/delete.html', context)

def edit(request):
    title = 'Edit Library Information'
    subtitle = 'List of libraries to edit be generated from library browser.'

    extras = 0

    pks = request.POST.getlist("selection")
    qset = Library.objects.filter(pk__in=pks)

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
        columns = ['parent_name', 'sample_type', 'conc', 'vol']
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
                sample_record = Sample.objects.get_or_create(name=sample_name)
                sample = sample_record[0]
                record['sample'] = sample.id
            extras = count


    LibraryFormSet = modelformset_factory(Library, form=LibraryForm, extra=extras)
    formset = LibraryFormSet(queryset=qset, initial=data)

    table = LibraryTable(Library.objects.filter(pk__in=pks))

    if "save_btn" in request.POST:
        formset = LibraryFormSet(request.POST)
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

        return HttpResponseRedirect('/library')

    context = {
        'button_type': 'buttons_1.html',
        'title': title,
        'subtitle': subtitle,
        # "basic_url": basic_url,
        # "advanced_url": advanced_url,
        "formset": formset,
        "table": table,
        "extras": extras,
        "upload_form": upload_form,
    }

    return render(request, 'library/edit.html', context)

##### Class based views

#### Libraries
## Library Browsers/FilterTables
# Browser/Table base
class LibraryTableBase(PagedFilteredTableView):
    template_name = 'library/selector.html'
    model = Library
    filter_class = LibraryListFilter
    formhelper_class = LibraryListFormHelper

    button_type = 'buttons_1.html'
    buttons = [
        {"name": 'Simple', "class": 'btn btn-default', "url": 'library:browser'},
        {"name": 'Plate Setup', "class": 'btn btn-default', "url": 'library:browser_plate'},
        {"name": 'QC', "class": 'btn btn-default', "url": 'library:browser_qc'},
        {"name": 'Full', "class": 'btn btn-default', "url": 'library:browser_full'},
    ]

    # TODO setup buttons so that None is an option
    def get_buttons(self):
        buttons = self.buttons
        page = self.page
        for button in buttons:
            if button['name'] == page:
                button['class'] = 'btn btn-success'
            else:
                button['class'] = 'btn btn-default'
        return buttons

# Table instances
class LibraryTableSimple(LibraryTableBase):
    title = 'Library Browser - Plate'
    page = 'Simple'
    table_class = LibraryTableSimple

class LibraryTablePlateSetup(LibraryTableBase):
    title = 'Library Browser - Plate Setup'
    page = 'Plate Setup'
    table_class = LibraryTablePlateSetup

class LibraryTableQC(LibraryTableBase):
    title = 'Library Browser - QC'
    page = 'QC'
    table_class = LibraryTableQC

class LibraryTableFull(LibraryTableBase):
    title = 'Library Browser - Full'
    page = 'Full'
    table_class = LibraryTableFull

## Library CreateViews
# CreateView base (inherits from LIMS Generic CreateView)
class LibraryCreateFormSetBase(GenericUpdateFormSet):
    template_name = 'library/create.html'
    success_url = reverse_lazy('library:browser')
    button_type = 'buttons_1.html'
    model = Library
    form_class = LibraryForm
    buttons = [
        {"name": 'Basic', "class": 'btn btn-default', "url": 'library:create'},
    ]
    extra = 5

    def get_buttons(self):
        buttons = self.buttons
        page = self.page
        for button in buttons:
            if button['name'] == page:
                button['class'] = 'btn btn-success'
            else:
                button['class'] = 'btn btn-default'

        return buttons

# CreateViews instances
class LibraryCreateFormSetBasic(LibraryCreateFormSetBase):
    title = 'Enter Library Setup Information'
    page = 'Basic'
    field = ('gtc_code', 'library_type', 'plate_name', 'well', 'parent_name', 'name', 'amount_of_sample_used',
             'amount_of_water_used', 'plate_comments')

## Library UpdateViews
# UpdateView Base
class LibraryUpdateFormSetBase(GenericUpdateFormSet):
    template_name = 'library/update.html'
    success_url = reverse_lazy('library:browser')
    button_type = 'buttons_3.html'
    model = Library
    model_parent = Sample
    form_class = LibraryForm
    buttons = [
        {"name": 'Plate', "class": 'btn btn-default', "url": 'library:update_plate'},
        {"name": 'QC', "class": 'btn btn-default', "url": 'library:update_qc'},
    ]

    def get_buttons(self):
        buttons = self.buttons
        page = self.page
        for button in buttons:
            if button['name'] == page:
                button['class'] = 'btn btn-success'
            else:
                button['class'] = 'btn btn-default'
        return buttons

class LibraryUpdateFormSetPlateSetup(LibraryUpdateFormSetBase):
    title = 'Edit Library Information - Plate Setup'
    page = 'Plate'
    field = ('unique_id', 'gtc_code', 'library_type', 'plate_name', 'well', 'parent_name', 'name',
             'amount_of_sample_used', 'amount_of_water_used', 'plate_comments')

class LibraryUpdateFormSetQC(LibraryUpdateFormSetBase):
    title = 'Edit Library Information - Final Library QC'
    page = 'QC'
    field = ('unique_id', 'gtc_code', 'library_type', 'plate_name', 'well', 'parent_name', 'name',
             'illumina_barcode_plate', 'barcode_well', 'i7_barcode', 'i5_barcode', 'library_amount',
             'tapestation_size_bp', 'tapestation_conc_ng_uL', 'tapestation_molarity_nM', 'qpcr_conc_molarity_nM', 'qubit_conc_ng_uL',
             )

## Library Delete
class LibraryTableDeleteBase(PagedFilteredTableView):
    template_name = 'library/delete.html'
    model = Library
    filter_class = LibraryListFilter
    formhelper_class = LibraryListFormHelper
    title = 'Are you sure you want to delete these samples?'
    page = 'Full'
    table_class = LibraryTableDelete #needs its own table - not sure why

    button_type = 'buttons_1.html'
    buttons = []

#### Pools
## Pool Browsers/FilterTables
# Browser Pool Base
class PoolTableBase(PagedFilteredTableView):
    template_name = 'library/selector_pool.html'
    model = Pool
    filter_class = PoolListFilter
    formhelper_class = PoolListFormHelper

    button_type = 'buttons_1.html'
    buttons = []

    # TODO setup buttons so that None is an option
    def get_buttons(self):
        buttons = self.buttons
        page = self.page
        for button in buttons:
            if button['name'] == page:
                button['class'] = 'btn btn-success'
            else:
                button['class'] = 'btn btn-default'
        return buttons

# Table instances
class PoolTableSimple(PoolTableBase):
    title = 'Pool Browser'
    page = 'Simple'
    table_class = PoolTable

### Pool UpdateViews
# UpdateView Base
class PoolUpdateFormSetBase(GenericUpdateFormSet):
    template_name = 'library/update_pool.html'
    success_url = reverse_lazy('library:pool_browser')
    button_type = 'buttons_3.html'
    model = PoolingAmount
    model_parent = Pool
    # TODO this 'form_classes' hack is a way to get around the single form_class restriction in django classes more appropriate handling is done by:
    # https://www.codementor.io/lakshminp/handling-multiple-forms-on-the-same-page-in-django-fv89t2s3j
    # https://stackoverflow.com/questions/15497693/django-can-class-based-views-accept-two-forms-at-a-time
    form_classes = {'form_current': PoolingAmountForm,
                    'model_current': PoolingAmount,
                    'form_parent': PoolForm,
                    'model_parent': Pool}
    # form_class = PoolForm

    buttons = [
        {"name": 'Plate', "class": 'btn btn-default', "url": 'library:update_plate'},
        {"name": 'QC', "class": 'btn btn-default', "url": 'library:update_qc'},
    ]

    def get_buttons(self):
        buttons = self.buttons
        page = self.page
        for button in buttons:
            if button['name'] == page:
                button['class'] = 'btn btn-success'
            else:
                button['class'] = 'btn btn-default'
        return buttons

class PoolUpdateFormSetPooling(PoolUpdateFormSetBase):
    title = 'Pooling'
    page = 'Plate'
    field = ('pool_name', 'library_name', 'name', 'rel_proportion', 'amount_of_library_used', 'library_amount')

### Pool Delete
class PoolTableDeleteBase(PagedFilteredTableView):
    template_name = 'library/delete.html'
    model = Pool
    filter_class = PoolListFilter
    formhelper_class = PoolListFormHelper
    title = 'Are you sure you want to delete these samples?'
    page = 'Full'
    table_class = PoolTable #needs its own table - not sure why

    button_type = 'buttons_1.html'
    buttons = []

#### PoolAmounts
### PoolAmounts - Table
class PoolingAmountTableBase(PagedFilteredTableView):
    template_name = 'library/selector_poolamount.html'
    model = PoolingAmount
    filter_class = PoolingAmountListFilter
    formhelper_class = PoolingAmountListFormHelper

    button_type = 'buttons_1.html'
    buttons = []

    # TODO setup buttons so that None is an option
    def get_buttons(self):
        buttons = self.buttons
        page = self.page
        for button in buttons:
            if button['name'] == page:
                button['class'] = 'btn btn-success'
            else:
                button['class'] = 'btn btn-default'
        return buttons

# PoolingAmounts - Table Instance
class PoolingAmountTableSimple(PoolingAmountTableBase):
    title = 'Pooling Amount Browser'
    page = 'Simple'
    table_class = PoolingAmountTable

### PoolingAmounts - Update
class PoolingAmountUpdateFormSetBase(GenericUpdateFormSet):
    template_name = 'library/update.html'
    success_url = reverse_lazy('library:browser')
    button_type = 'buttons_3.html'
    model = PoolingAmount
    model_parent = Pool
    form_class = PoolingAmountForm
    buttons = []

    def get_buttons(self):
        buttons = self.buttons
        page = self.page
        for button in buttons:
            if button['name'] == page:
                button['class'] = 'btn btn-success'
            else:
                button['class'] = 'btn btn-default'
        return buttons

class PoolingAmountUpdateFormSetPooling(PoolingAmountUpdateFormSetBase):
    title = 'Edit Pooling Amount Information'
    page = 'Plate'
    field = ('pool_name', 'library_name', 'name', 'rel_proportion', 'amount_of_library_used', 'library_amount')


### Pool Delete
class PoolAmountTableDeleteBase(PagedFilteredTableView):
    template_name = 'library/delete.html'
    model = PoolingAmount
    filter_class = PoolingAmountListFilter
    formhelper_class = PoolingAmountListFormHelper
    title = 'Are you sure you want to delete these pooling amounts?'
    page = 'Full'
    table_class = PoolingAmountTable #needs its own table - not sure why

    button_type = 'buttons_1.html'
    buttons = []


### archived views
def lib_browser(request):
    title = 'Library Browser'
    basic_url = 'library:browser'
    advanced_url = 'library:browser'

    qset = Library.objects.all()
    filter = LibraryFilter(request.GET, queryset=qset)
    table = LibraryTable(filter.qs)

    if "basic" in request.POST:
        table = LibraryTable(filter.qs)

    if "advanced" in request.POST:
        table = LibraryTable(filter.qs)

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

    return render(request, 'library/browser.html', context)

def add(request):
    title = 'Enter Plating Information for Processing Sample'
    subtitle = 'List of samples to submit to library making can be generated from sample browser.'
    # basic_url = 'library:add'
    # advanced_url = 'library:add'
    data = ()
    upload_form = UploadFileForm()
    pks = request.POST.getlist("selection")
    libraries = []

    if len(pks) < 1:
        extras = 5
    else:
        extras = 0
        for pk in pks:
            print(pk)
            sample = Sample.objects.get(pk=pk)
            lib_name = str(sample)+'_'+str(date_stamp)
            Library.objects.create(parent_name=sample, name=lib_name)
            libraries.append(lib_name)

    qset = Library.objects.filter(name__in=libraries)


    if "export_btn" in request.POST:
        # from https://simpleisbetterthancomplex.com/tutorial/2016/07/29/how-to-export-to-excel.html
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="libraries.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Library')
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        # TODO make dynamic columns
        columns = ['gtc_code', 'library_type', 'plate_name', 'well', 'parent_name', 'name', 'amount_of_sample_used', 'amount_of_water_used', 'plate_comments',]
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        wb.save(response)
        return response

    if "upload_btn" in request.POST:
        upload_form = UploadFileForm(request.POST, request.FILES)
        if upload_form.is_valid():
            filehandle = request.FILES['myfile']
            data = filehandle.get_records()
            count = 0
            for record in data:
                count = count + 1
                library_name = record['name']
                # TODO figure out how to prevent saving when uploading
                # TODO get_or_create from samples
                library_record = Library.objects.get_or_create(name=library_name)
                library = library_record[0]
                record['library'] = library.id
            extras = count
    #
    #
    LibraryFormSet = modelformset_factory(Library, form=LibraryPlateForm, extra=extras)
    formset = LibraryFormSet(queryset=qset, initial=data)

    table = LibraryTable(Library.objects.all())

    if "save_btn" in request.POST:
        formset = LibraryFormSet(request.POST)
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

        return HttpResponseRedirect('/library')

    context = {
        'button_type': 'buttons_1.html',
        'title': title,
        'subtitle': subtitle,
        # "basic_url": basic_url,
        # "advanced_url": advanced_url,
        "formset": formset,
        "table": table,
        "extras": extras,
        "upload_form": upload_form,
    }

    return render(request, 'library/add.html', context)

def validate(request):
    title = 'Validate/QC Libraries'
    basic_url = 'library:validate'
    advanced_url = 'library:validate'
    data = ()
    upload_form = UploadFileForm()
    pks = request.POST.getlist("selection")

    if len(pks) < 1:
        extras = 1
    else:
        extras = 0

    qset = Library.objects.filter(pk__in=pks)


    if "export_btn" in request.POST:
        # from https://simpleisbetterthancomplex.com/tutorial/2016/07/29/how-to-export-to-excel.html
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="libraries.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Library')
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        # TODO make dynamic columns
        columns = [
            'library_type', 'plate_name', 'well', 'parent_name', 'name',
            'illumina_barcode_plate', 'barcode_well', 'i7_barcode', 'i5_barcode', 'library_amount', 'tapestation_size_bp',
            'tapestation_conc', 'tapestation_molarity_nM', 'qpcr_conc', 'qubit_conc',
        ]
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        wb.save(response)
        return response

    if "upload_btn" in request.POST:
        upload_form = UploadFileForm(request.POST, request.FILES)
        if upload_form.is_valid():
            filehandle = request.FILES['myfile']
            data = filehandle.get_records()
            count = 0
            for record in data:
                count = count + 1
                library_name = record['name']
                # TODO figure out how to prevent saving when uploading
                # TODO get_or_create from samples
                library_record = Library.objects.get_or_create(name=library_name)
                library = library_record[0]
                record['library'] = library.id
            extras = count

    LibraryFormSet = modelformset_factory(Library, form=LibraryValidateForm, extra=extras)
    formset = LibraryFormSet(queryset=qset, initial=data)

    table = LibraryTable(Library.objects.all())

    if "save_btn" in request.POST:
        formset = LibraryFormSet(request.POST)
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

        return HttpResponseRedirect('/library/browser')

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

    return render(request, 'library/add.html', context)

def pool_browser(request):
    title = 'Pool Browser'
    basic_url = 'library:pool_browser'
    advanced_url = 'library:pool_browser'

    qset = Pool.objects.all()
    filter = PoolFilter(request.GET, queryset=qset)
    table = PoolTable(filter.qs)


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

    return render(request, 'library/browser_pool.html', context)

def pool(request):
    title = 'Pool Libraries'
    data = ()
    upload_form = UploadFileForm()
    pks = request.POST.getlist("selection")

    if len(pks) < 1:
        extras = 5
        pool_name = []
        form_p = PoolForm
        qset = PoolingAmount.objects.none()

    else:
        extras = 0
        pool_name_sm = 'pool_' + str(date_stamp)
        num_results = Pool.objects.filter(name__contains=pool_name_sm).count()
        pool_name = pool_name_sm + '_0' + str(num_results + 1)
        pool = Pool.objects.create(name=pool_name)
        print('===========pool===========')
        print(pool)

        for pk in pks:
            library = Library.objects.get(pk=pk)
            print('=============library=============')
            print(library)
            PoolingAmount.objects.create(library_name=library, pool_name=pool)

        form_p = PoolForm(instance=Pool.objects.get(name=pool_name))
        qset = PoolingAmount.objects.filter(pool_name=pool)

    if "quantity" in request.POST:
        extras = int(request.POST['quantity'])

    # if "export_btn" in request.POST:
    #     # from https://simpleisbetterthancomplex.com/tutorial/2016/07/29/how-to-export-to-excel.html
    #     response = HttpResponse(content_type='application/ms-excel')
    #     response['Content-Disposition'] = 'attachment; filename="libraries.xls"'
    #     wb = xlwt.Workbook(encoding='utf-8')
    #     ws = wb.add_sheet('Library')
    #     row_num = 0
    #     font_style = xlwt.XFStyle()
    #     font_style.font.bold = True
    #     # TODO make dynamic columns
    #     columns = ['gtc_code', 'library_type', 'plate_name', 'well', 'sample_name', 'library_name', 'amount_of_sample_used', 'amount_of_water_used', 'plate_comments',]
    #     for col_num in range(len(columns)):
    #         ws.write(row_num, col_num, columns[col_num], font_style)
    #     wb.save(response)
    #     return response
    #
    # if "upload_btn" in request.POST:
    #     upload_form = UploadFileForm(request.POST, request.FILES)
    #     if upload_form.is_valid():
    #         filehandle = request.FILES['myfile']
    #         data = filehandle.get_records()
    #         count = 0
    #         for record in data:
    #             count = count + 1
    #             pool_name = record['pool_name']
    #             # TODO figure out how to prevent saving when uploading
    #             # TODO get_or_create from samples
    #             pool_record = Pool.objects.get_or_create(pool_name=pool_name)
    #             pool = pool_record[0]
    #             record['pool'] = pool.id
    #         extras = count

    PoolingFormSet = modelformset_factory(PoolingAmount, form=PoolingAmountForm, extra=extras)
    formset = PoolingFormSet(queryset=qset, initial=data)

    print('----------------formset--------------')

    table = PoolTable(Pool.objects.all())

    # TODO add save back in and use pool name from parent form for pool_name in formset

    if "save_btn" in request.POST:
        formset = PoolingFormSet(request.POST)
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

        return HttpResponseRedirect('/library/pool_browser')

    context = {
        'button_type': 'buttons_1.html',
        'title': title,
        # "basic_url": basic_url,
        # "advanced_url": advanced_url,
        "form_p": form_p,
        "formset": formset,
        # "table": table,
        # "extras": extras,
        # "upload_form": upload_form,
    }

    return render(request, 'library/add_pool.html', context)

def delete(request):
    title = 'Are you sure you want to delete the following libraries?'
    pks = request.POST.getlist("selection")
    library = Library.objects.filter(pk__in=pks)
    table = LibraryTable(Library.objects.filter(pk__in=pks))

    if request.method == "POST":
        if "del_confirm_btn" in request.POST:
            num_deleted = len(pks)
            library.delete()
            messages.warning(request, '%d libraries deleted.' %num_deleted)
            return HttpResponseRedirect('/library')
        if "no_btn" in request.POST:
            messages.success(request, 'No libraries were deleted.')
            return HttpResponseRedirect('/library')

    context = {
        # "add_url": add_url,
        # "select_url": select_url,
        "title": title,
        "table": table,
        # "num_deleted": num_deleted,
    }
    return render(request, 'library/delete.html', context)

def test(request):

    form = PoolForm

    context = {
        "form": form,
    }
    return render(request, 'test.html', context)