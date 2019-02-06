from django.shortcuts import render
from django.forms import modelformset_factory, formset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

from .models import Library, Pool, PoolingAmount
from .forms import UploadFileForm, LibraryPlateForm, LibraryValidateForm, PoolForm, AddressForm, PoolingAmountForm
from .tables import LibraryTable, PoolTable
from .filters import LibraryFilter, PoolFilter
from sample.models import Sample

import datetime

# for working with excel in exports and imports
import xlwt
import csv


# time stamp
now = datetime.datetime.now()
date_stamp = now.strftime("%d%m%Y")

def test(request):

    form = PoolForm

    context = {
        "form": form,
    }
    return render(request, 'test.html', context)

# TODO move redundant view defs to common folder
def add(request):
    title = 'Enter Plating Information for Processing Sample'
    basic_url = 'library:add'
    advanced_url = 'library:add'
    data = ()
    upload_form = UploadFileForm()
    pks = request.POST.getlist("selection")
    libraries = []

    if len(pks) < 1:
        extras = 1
    else:
        extras = 0

    for pk in pks:
        print(pk)
        sample = Sample.objects.get(pk=pk)
        lib_name = str(sample)+'_'+str(date_stamp)
        Library.objects.create(sample_name=sample, library_name=lib_name)
        libraries.append(lib_name)

    qset = Library.objects.filter(library_name__in=libraries)


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
        columns = ['gtc_code', 'library_type', 'plate_name', 'well', 'sample_name', 'library_name', 'amount_of_sample_used', 'amount_of_water_used', 'plate_comments',]
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
                library_name = record['library_name']
                # TODO figure out how to prevent saving when uploading
                # TODO get_or_create from samples
                library_record = Library.objects.get_or_create(library_name=library_name)
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
        "basic_url": basic_url,
        "advanced_url": advanced_url,
        "formset": formset,
        "table": table,
        "extras": extras,
        "upload_form": upload_form,
    }

    return render(request, 'library/add.html', context)

def lib_browser(request):
    title = 'Library Browser'
    basic_url = 'library:lib_browser'
    advanced_url = 'library:lib_browser'

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


def delete(request):
    title = 'Are you sure you want to delete the following samples?'
    pks = request.POST.getlist("selection")
    library = Library.objects.filter(pk__in=pks)
    table = LibraryTable(Library.objects.filter(pk__in=pks))

    if request.method == "POST":
        if "del_confirm_btn" in request.POST:
            num_deleted = len(pks)
            library.delete()
            messages.warning(request, '%d library deleted.' %num_deleted)
            return HttpResponseRedirect('/library')
        if "no_btn" in request.POST:
            messages.success(request, 'No records were deleted.')
            return HttpResponseRedirect('/library')

    context = {
        # "add_url": add_url,
        # "select_url": select_url,
        "title": title,
        "table": table,
        # "num_deleted": num_deleted,
    }
    return render(request, 'library/delete.html', context)

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
            'library_type', 'plate_name', 'well', 'sample_name', 'library_name',
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
                library_name = record['library_name']
                # TODO figure out how to prevent saving when uploading
                # TODO get_or_create from samples
                library_record = Library.objects.get_or_create(library_name=library_name)
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
        num_results = Pool.objects.filter(pool_name__contains=pool_name_sm).count()
        pool_name = pool_name_sm + '_0' + str(num_results + 1)
        pool = Pool.objects.create(pool_name=pool_name)

        for pk in pks:
            library = Library.objects.get(pk=pk)
            PoolingAmount.objects.create(library_name=library, pool_name=pool)

        form_p = PoolForm(instance=Pool.objects.get(pool_name=pool_name))
        qset = PoolingAmount.objects.filter(pool_name=pool)

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

    # if "save_btn" in request.POST:
    #     formset = PoolFormSet(request.POST)
    #     if formset.is_valid():
    #         record_num = int(0)
    #         record_add = int(0)
    #         for form in formset:
    #             record_num += 1
    #             if form.is_valid():
    #                 if form.cleaned_data == {}:
    #                     messages.warning(request, 'Record #%d did not add because required data was missing.' % record_num)
    #                 else:
    #                     record_add += 1
    #                     form.save()
    #             else:
    #                 messages.warning(request, 'Form Error')
    #         messages.success(request, '%d records added successfully.' % record_add)
    #     else:
    #         messages.warning(request, 'Formset Error')
    #
    #     return HttpResponseRedirect('/library/browser')

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