from django.shortcuts import render
from django.forms import modelformset_factory, formset_factory
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.urls import reverse_lazy

from LIMS.views import GenericUpdateFormSet, PagedFilteredTableView
from .forms import WUSSubmissionForm, WUSPoolForm, WUSSubmissionListFormHelper, WUSPoolListFormHelper, WUSResultListFormHelper, WUSResultForm
from .models import WUSSubmission, WUSPool, WUSSampleResult, WUSResult
from .filters import WUSResultFilter, WUSSubmissionFilter, WUSSubmissionListFilter, WUSPoolListFilter
from .tables import WUSResultsTable, WUSSubmissionTable, WUSPoolTable

from library.models import Library, Pool, PoolingAmount
from library.forms import UploadFileForm, LibraryPlateForm, LibraryValidateForm, PoolForm, PoolingAmountForm, LibraryForm, LibraryListFormHelper, PoolListFormHelper, PoolingAmountListFormHelper
from library.tables import LibraryTableSimple, LibraryTableDelete, LibraryTablePlateSetup, LibraryTableQC, LibraryTable, LibraryTableFull, PoolTable, PoolingAmountTable
from library.filters import LibraryListFilter, LibraryFilter, PoolListFilter, PoolFilter, PoolingAmountListFilter

import datetime
import math

# for working with excel in exports and imports
import xlwt
import csv


# time stamp
now = datetime.datetime.now()
date_stamp = now.strftime("%d%m%Y")

##### Class based views

### WUSSubmission
## WUSSubmission Tables/Browsers
class WUSSubmissionTableBase(PagedFilteredTableView):
    template_name = 'selector.html'
    model = WUSSubmission
    filter_class = WUSSubmissionListFilter
    formhelper_class = WUSSubmissionListFormHelper

    button_type = 'buttons_1.html'
    buttons = []
    buttons_processing_type = 'buttons_processing.html'
    buttons_processing = [
        {"name": 'update_2_form_btn', "class":'btn btn-primary', "url": 'sequence:submission_update', "value": 'Update Submission'},
        {"name": 'update_btn', "class": 'btn btn-warning', "url": 'sequence:submission_create', "value": 'New Submission'},
        {"name": 'generate_btn', "class": 'btn btn-secondary', "url": 'sequence:update_result', "value": 'Generate WUS Metrics'},
        {"name": 'del_btn', "class":'btn btn-danger', "url": 'sequence:submission_delete', "value": 'Delete'},
    ]

    # TODO setup buttons so that None is an option


# Table instances
class WUSSubmissionTableSimpleView(WUSSubmissionTableBase):
    title = 'WUS Submissions'
    page = 'Simple'
    table_class = WUSSubmissionTable

## Create Base
class WUSSubmissionCreateFormSetBase(GenericUpdateFormSet):
    template_name = 'update.html'
    success_url = reverse_lazy('sequence:browser_pool')
    button_type = 'buttons_3.html'
    model = WUSSubmission
    model_parent = Pool
    form_class = WUSSubmissionForm
    buttons = []
    buttons_processing_type = 'buttons_processing.html'
    buttons_processing = [
        {"name": 'save_btn', "class": 'btn btn-primary', "value": 'Update WUS Pool', "url": 'sequence:wus_pool'},
    ]


## UpdateView Base
class WUSSubmissionUpdateFormSetBase(GenericUpdateFormSet):
    template_name = 'form_twoforms.html'
    success_url = reverse_lazy('sequence:browser')
    button_type = 'buttons_3.html'
    batch_prefix = 'wus'
    record_prefix = 'wp'
    # TODO this 'form_classes' hack is a way to get around the single form_class restriction in django classes more appropriate handling is done by:
    # https://www.codementor.io/lakshminp/handling-multiple-forms-on-the-same-page-in-django-fv89t2s3j
    # https://stackoverflow.com/questions/15497693/django-can-class-based-views-accept-two-forms-at-a-time
    form_classes = {'form_current': WUSPoolForm,
                    'model_current': WUSPool,
                    'form_parent': WUSSubmissionForm,
                    'model_parent': WUSSubmission,
                    'form_related': PoolForm,
                    'model_related': Pool}
    # form_class = PoolForm

    buttons = []
    buttons_processing_type = 'buttons_processing.html'
    buttons_processing = [
        {"name": 'save_btn',  "class":'btn btn-primary', "value": 'Update WUS Pools', "url": 'sequence:wus_pool'},
    ]


# Update - Instances
class WUSSubmissionCreateFormSetPooling(WUSSubmissionUpdateFormSetBase):
    template_name = 'form_simple.html'
    title = 'WUS Submissions - Create New Submissions'
    page = 'Plate'
    field = ('unique_id', 'related_name', 'parent_name', 'num_of_lanes')
    form_class = WUSPoolForm
    extra = 5
    objects = None

class WUSSubmissionUpdateFormSetPooling(WUSSubmissionUpdateFormSetBase):
    title = 'WUS Submissions'
    page = 'Plate'
    field = ('unique_id', 'related_name', 'parent_name', 'num_of_lanes')


## DeleteView Base
class WUSSubmissionTableDeleteBase(PagedFilteredTableView):
    template_name = 'delete.html'
    model = WUSSubmission
    filter_class = WUSSubmissionListFilter
    formhelper_class = WUSSubmissionListFormHelper
    title = 'Are you sure you want to delete these WUS Submissions?'
    page = 'Full'
    table_class = WUSSubmissionTable
    button_type = 'buttons_1.html'
    buttons = []
    buttons_processing_type = 'buttons_processing.html'
    buttons_processing = [
        {"name": 'del_confirm_btn',  "class":'btn btn-danger', "url": 'sequence:browser', "value": 'Delete WUS Submission'},
        {"name": 'cancel_btn',  "class":'btn btn-primary', "url": 'sequence:browser', "value": 'Cancel'},
    ]

### WUSPools
## WUSPool Tables/Browsers
class WUSPoolTableBase(PagedFilteredTableView):
    template_name = 'selector.html'
    model = WUSPool
    filter_class = WUSPoolListFilter
    formhelper_class = WUSPoolListFormHelper

    button_type = 'buttons_1.html'
    buttons = []
    buttons_processing_type = 'buttons_processing.html'
    buttons_processing = [
        {"name": 'edit_btn',  "class":'btn btn-primary', "url": 'sequence:wus_pool', "value": 'Update WUS Pool'},
        {"name": 'del_btn',  "class":'btn btn-danger', "url": 'sequence:wuspool_delete', "value": 'Delete'},
    ]

# Table instances
class WUSPoolTableSimpleView(WUSPoolTableBase):
    title = 'WUS Pools'
    page = 'Simple'
    table_class = WUSPoolTable


# WUSPool Update
class WUSPoolUpdateFormSetBase(GenericUpdateFormSet):
    template_name = 'update.html'
    success_url = reverse_lazy('sequence:browser_pool')
    button_type = 'buttons_3.html'
    model = WUSPool
    model_parent = WUSSubmission
    form_class = WUSPoolForm
    buttons = []
    buttons_processing_type = 'buttons_processing.html'
    buttons_processing = [
        {"name": 'save_btn', "class": 'btn btn-primary', "value": 'Update WUS Pool', "url": 'sequence:wus_pool'},
    ]

class WUSPoolUpdateFormSetPooling(WUSPoolUpdateFormSetBase):
    title = 'Edit Pooling Amount Information'
    page = 'Plate'
    field = ('unique_id', 'related_name', 'parent_name', 'num_of_lanes')

## Delete Base
class WUSPoolTableDeleteBase(PagedFilteredTableView):
    template_name = 'delete.html'
    model = WUSPool
    filter_class = WUSPoolListFilter
    formhelper_class = WUSPoolListFormHelper
    title = 'Are you sure you want to delete these WUS pools?'
    page = 'Full'
    table_class = WUSPoolTable
    button_type = 'buttons_1.html'
    buttons = []
    buttons_processing_type = 'buttons_processing.html'
    buttons_processing = [
        {"name": 'del_confirm_btn',  "class": 'btn btn-danger', "url": 'sequence:browser_pool', "value": 'Delete WUS Pools'},
        {"name": 'cancel_btn',  "class": 'btn btn-primary', "url": 'sequence:browser_pool', "value": 'Cancel'},
    ]

### WUSResults
## WUSResults Tables/Browsers
class WUSResultBase(PagedFilteredTableView):
    template_name = 'selector.html'
    model = WUSResult
    filter_class = WUSResultFilter
    formhelper_class = WUSResultListFormHelper

    button_type = 'buttons_1.html'
    buttons = []
    buttons_processing_type = 'buttons_processing.html'
    buttons_processing = [
        {"name": 'edit_btn',  "class":'btn btn-primary', "url": 'sequence:update_result', "value": 'Update WUS Results'},
        {"name": 'del_btn',  "class":'btn btn-danger', "url": 'library:library_delete', "value": 'Delete'},
    ]


# Table instances
class WUSResultTableSimpleView(WUSResultBase):
    title = 'WUSResults Browser'
    page = 'Simple'
    table_class = WUSResultsTable

# CreateView
class WUSResultCreateFormSetBase(GenericUpdateFormSet):
    template_name = 'update.html'
    success_url = reverse_lazy('sequence:browser_result')
    button_type = 'buttons_1.html'
    model = WUSResult
    model_parent = WUSPool
    form_class = WUSResultForm
    buttons = []

    buttons_processing_type = 'buttons_processing.html'
    buttons_processing = [
        {"name": 'save_btn', "class": 'btn btn-primary', "value": 'Add', "url": 'sequence:create_result'},
    ]

# CreateViews instances
class WUSResultCreateFormSetBasic(WUSResultCreateFormSetBase):
    title = 'Enter WUSResult - Basic Information'
    page = 'Basic'
    field = ('broad_id', 'parent_name', 'related_name', 'lane_number', 'barcode', 'read', 'fastq_name', 'counts')
    extra = 5
    buttons_processing = [
        {"name": 'save_btn', "class": 'btn btn-primary', "value": 'Add', "url": 'sequence:create_result'},
    ]

class WUSResultUpdateFormSetBasic(WUSResultCreateFormSetBase):
    title = 'Enter WUSResult - Basic Information'
    page = 'Basic'
    field = ('unique_id', 'broad_id', 'parent_name', 'related_name', 'lane_number', 'barcode', 'read', 'fastq_name', 'counts')
    buttons_processing = [
        {"name": 'save_btn', "class": 'btn btn-primary', "value": 'Update', "url": 'sequence:create_result'},
    ]

    def get_lanes(self, request):
        print('===============get_lanes=====================')
        parent_pks = request.POST.getlist("selection")
        print(parent_pks)
        pks = []

        # get only first "parent pk"
        # TODO DRY used multiple times, update_2_form_btn
        if len(parent_pks) > 1:
            messages.warning(request, 'Only first record chosen can be displayed')
            self.parent_pks = parent_pks
        elif len(parent_pks) < 1:
            self.parent_pks = []
            messages.warning(request, 'No records were selected.')
        else:
            self.parent_pks = parent_pks

        if self.parent_pks:
            parent_pk = self.parent_pks[0]
            wus_pools = WUSPool.objects.filter(parent_name=parent_pk)
            broad_id = WUSSubmission.objects.filter(pk=parent_pk)[0].broad_id

            lane_counter = 0
            for pool in wus_pools:
                pa = PoolingAmount.objects.filter(parent_name=pool.related_name)

                if pool.num_of_lanes:
                    print(pool)
                    print(pool.num_of_lanes)
                    pool_lanes = pool.num_of_lanes
                    for lane in range(math.floor(lane_counter), math.ceil(pool_lanes)):
                        print('========lane number==================')
                        print(lane+1)
                        for lib_id in pa:
                            lib = lib_id.related_name
                            if lib.i7_barcode:
                                if lib.i5_barcode:
                                    lib_barcode = str(lib.i7_barcode) + '_' + str(lib.i5_barcode)
                                else:
                                    lib_barcode = str(lib.i7_barcode)
                            else:
                                lib_barcode = None
                                messages.warning(request, 'Record %s did not have any barcodes.' % lib)

                            if WUSSubmission.objects.filter(pk=parent_pk)[0].dual_barcode:
                                print('parent_name = %s, related_name = %s, broad_id = %s, lane = %s, library = %s, barcode = %s, read = %s' % (
                                    pool, lib, broad_id, str(lane + 1), lib.name, lib_barcode, 'R1'))
                                new_result = WUSResult.objects.create(parent_name=pool, related_name=lib, lane_number=int(lane+1),
                                                       barcode=lib_barcode, broad_id=broad_id, read='R1')
                                pks.append(new_result.pk)
                                print('broad_id = %s, lane = %s, library = %s, barcode = %s, read = %s' % (
                                    broad_id, str(lane + 1), lib.name, lib_barcode, 'R2'))
                                new_result = WUSResult.objects.create(parent_name=pool, related_name=lib, lane_number=int(lane+1),
                                                       barcode=lib_barcode, broad_id=broad_id, read='R2')
                                pks.append(new_result.pk)

                            else:
                                print('broad_id = %s, lane = %s, library = %s, barcode = %s, read = %s' % (
                                    broad_id, str(lane + 1), lib.name, lib_barcode, 'R1'))
                                new_result = WUSResult.objects.create(parent_name=pool, related_name=lib, lane_number=int(lane+1),
                                                       barcode=lib_barcode, broad_id=broad_id, read='R1')
                                pks.append(new_result.pk)

                            # print('broad_id = %s, lane = %s, library = %s, barcode = %s' % (broad_id, str(lane+1), lib.name, lib_barcode))
                            # WUSResult.model.create(parent_name=pk, name=lib_name)
                    lane_counter = lane_counter + pool_lanes
                    print('lane_counter = %d' % lane_counter)
                else:
                    messages.warning(request, 'Record %s did not have num of lanes designated.' % pool)

            if (lane_counter).is_integer():
                print("integer")
            else:
                messages.error(request, 'A lane is only partially filled.')

        else:
            parent_pk = []
            pass


        test = '================end of get_lanes============='
        return request, parent_pk, pks, test


#### archived views
def test(request):

    form = WUSSubmissionForm

    context = {
        "form": form,
    }
    return render(request, 'sequence/test.html', context)

class testclass(View):
    form_class = WUSSubmissionForm
    template_name = 'sequence/test.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        pass

def browser(request):
    title = 'WUS Browser'
    basic_url = 'sequence:browser'
    advanced_url = 'sequence:browser'

    qset = WUSSubmission.objects.all()
    filter = WUSSubmissionFilter(request.GET, queryset=qset)
    table = WUSSubmissionTable(filter.qs)


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

    return render(request, 'sequence/browser.html', context)

def add(request):
    title = 'Enter New WUS Submission'
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

def add_wus_sub(request):
    title = 'WUS Submissions'
    data = ()
    # upload_form = UploadFileForm()
    pks = request.POST.getlist("selection")

    if len(pks) < 1:
        extras = 5
        wus_name = []
        form_p = WUSSubmissionForm
        qset = WUSPool.objects.none()

    else:
        extras = 0
        wus_name_sm = 'WUS_' + str(date_stamp)
        num_results = WUSSubmission.objects.filter(wus_name__contains=wus_name_sm).count()
        wus_name = wus_name_sm + '_0' + str(num_results + 1)
        wus_sub = WUSSubmission.objects.create(wus_name=wus_name)

        for pk in pks:
            pool = Pool.objects.get(pk=pk)
            WUSPool.objects.create(pool_name=pool, wus_name=wus_sub)

        form_p = WUSSubmissionForm(instance=WUSSubmission.objects.get(wus_name=wus_name))
        qset = WUSPool.objects.filter(wus_name=wus_sub)

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
    #             wus_sub_name = record['wus_sub_name']
    #             # TODO figure out how to prevent saving when uploading
    #             # TODO get_or_create from samples
    #             pool_record = WUSSubmission.objects.get_or_create(wus_sub_name=wus_sub_name)
    #             pool = pool_record[0]
    #             record['pool'] = pool.id
    #         extras = count

    WUSPoolFormSet = modelformset_factory(WUSPool, form=WUSPoolForm, extra=extras)
    formset = WUSPoolFormSet(queryset=qset, initial=data)

    print('----------------formset--------------')

    table = WUSSubmissionTable(WUSSubmission.objects.all())

    # TODO add save back in and use wus_sub name from parent form for wus_sub_name in formset

    if "save_btn" in request.POST:
        formset = WUSPoolFormSet(request.POST)
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

        return HttpResponseRedirect('/sequence/browser')

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

def edit(request):
    title = 'Edit WUS Submission Information'
    subtitle = 'List of WUS Submission to edit can be generated from library browser.'

    extras = 0

    pks = request.POST.getlist("selection")
    qset = WUSSubmission.objects.filter(pk__in=pks)

    data = ()
    # upload_form = UploadFileForm()

    # if "export_btn" in request.POST:
    #     # from https://simpleisbetterthancomplex.com/tutorial/2016/07/29/how-to-export-to-excel.html
    #     response = HttpResponse(content_type='application/ms-excel')
    #     response['Content-Disposition'] = 'attachment; filename="samples.xls"'
    #     wb = xlwt.Workbook(encoding='utf-8')
    #     ws = wb.add_sheet('Sample')
    #     row_num = 0
    #     font_style = xlwt.XFStyle()
    #     font_style.font.bold = True
    #     # TODO make dynamic columns
    #     columns = ['sample_name', 'sample_type', 'conc', 'vol']
    #     for col_num in range(len(columns)):
    #         ws.write(row_num, col_num, columns[col_num], font_style)
    #     wb.save(response)
    #     return response
    #
    # if "upload_btn" in request.POST:
    #     upload_form = UploadFileForm(request.POST, request.FILES)
    #     if upload_form.is_valid():
    #         print("valid")
    #         filehandle = request.FILES['myfile']
    #         data = filehandle.get_records()
    #         count = 0
    #         for record in data:
    #             count = count + 1
    #             sample_name = record['sample_name']
    #             # TODO figure out how to prevent saving when uploading
    #             sample_record = Sample.objects.get_or_create(sample_name=sample_name)
    #             sample = sample_record[0]
    #             record['sample'] = sample.id
    #         extras = count


    WUSSubmissionFormSet = modelformset_factory(WUSSubmission, form=WUSSubmissionForm, extra=extras)
    formset = WUSSubmissionFormSet(queryset=qset, initial=data)

    table = WUSSubmissionTable(WUSSubmission.objects.filter(pk__in=pks))

    if "save_btn" in request.POST:
        formset = WUSSubmissionFormSet(request.POST)
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
            messages.success(request, '%d records edited successfully.' % record_add)
        else:
            messages.warning(request, 'Formset Error')

        return HttpResponseRedirect('/sequence/browser')

    context = {
        'button_type': 'buttons_1.html',
        'title': title,
        'subtitle': subtitle,
        # "basic_url": basic_url,
        # "advanced_url": advanced_url,
        "formset": formset,
        "table": table,
        "extras": extras,
        # "upload_form": upload_form,
    }

    return render(request, 'sample/edit.html', context)

def delete(request):
    title = 'Are you sure you want to delete the following WUS submissions?'
    pks = request.POST.getlist("selection")
    wus_sub = WUSSubmission.objects.filter(pk__in=pks)
    table = WUSSubmissionTable(WUSSubmission.objects.filter(pk__in=pks))

    if request.method == "POST":
        if "del_confirm_btn" in request.POST:
            num_deleted = len(pks)
            wus_sub.delete()
            messages.warning(request, '%d WUS submissions deleted.' %num_deleted)
            return HttpResponseRedirect('/sequence/browser')
        if "no_btn" in request.POST:
            messages.success(request, 'No WUS submissions were deleted.')
            return HttpResponseRedirect('/sequence/browser')

    context = {
        # "add_url": add_url,
        # "select_url": select_url,
        "title": title,
        "table": table,
        # "num_deleted": num_deleted,
    }
    return render(request, 'library/delete.html', context)
