from django.shortcuts import render
from django.forms import modelformset_factory, formset_factory
from .models import Library
from .forms import UploadFileForm, LibraryForm
from .tables import LibraryTable
from sample.models import Sample

import datetime

# time stamp
now = datetime.datetime.now()
date_stamp = now.strftime("%d%m%Y")

def test(request):

    context = {
    }
    return render(request, 'test.html', context)

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


    # print(sample)
    # print(len(sample))

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
    #
    #
    LibraryFormSet = modelformset_factory(Library, form=LibraryForm, extra=extras)
    formset = LibraryFormSet(queryset=qset, initial=data)

    table = LibraryTable(Library.objects.all())

    # if "save_btn" in request.POST:
    #     formset = SampleFormSet(request.POST)
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
    #     return HttpResponseRedirect('/sample')

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
