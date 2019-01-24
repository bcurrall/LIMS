from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.forms import modelformset_factory
from .models import Sample
from .forms import UploadFileForm, SampleForm
from .tables import SampleTableBasic

# for working with excel in exports and imports
import xlwt
import csv

#test imports
from django.contrib.auth.models import User


# landing page for samples and browser for sample list
def browser(request):
    title = 'Enter Basic Samples Information'
    basic_url = 'sample:browser'
    advanced_url = 'sample:browser'
    # extras = 5
    # pks = list()
    # qset = Sample.objects.none()
    # data = ()
    # upload_form = UploadFileForm()

    table = SampleTableBasic(Sample.objects.all())

    context = {
        'button_type': 'buttons_1.html',
        'title': title,
        "basic_url": basic_url,
        "advanced_url": advanced_url,
        # "formset": formset,
        "table": table,
        # "extras": extras,
        # "upload_form": upload_form,
    }

    return render(request, 'sample/browser.html', context)

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
        for form in formset:
            if form.is_valid():
                entered_sample = form.save()
                pk = entered_sample.pk
                pks.append(pk)
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

### add sample
# add single new 01_10_19


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