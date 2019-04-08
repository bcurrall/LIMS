from django.shortcuts import render
from django.forms import modelformset_factory, formset_factory
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View


from .forms import WUSSubmissionForm, WUSPoolForm
from .models import WUSSubmission, WUSLaneResult, WUSPool, WUSSampleResult
from .filters import WUSLaneResultFilter, WUSSubmissionFilter
from .tables import WUSLaneResultsTable, WUSSubmissionTable
from library.models import Pool

import datetime

# for working with excel in exports and imports
import xlwt
import csv


# time stamp
now = datetime.datetime.now()
date_stamp = now.strftime("%d%m%Y")


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
