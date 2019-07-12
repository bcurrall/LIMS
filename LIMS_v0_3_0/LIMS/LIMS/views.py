# this views in LIMS app is only for generic views
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View, DeleteView, CreateView, FormView, UpdateView
from django.forms import modelformset_factory
from django.contrib import messages

from .forms import UploadFileForm

import xlwt

# TODO combine create and update views
# TODO make unique id -> currently relying on unique sample_name
class GenericCreateFormSet(CreateView):
    # class defaults
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
        context = super(GenericCreateFormSet, self).get_context_data(**kwargs)
        formset = self.get_formset()
        queryset = self.model.objects.none()
        context['formset'] = formset(queryset=queryset, initial=self.initial_data)
        context['title'] = self.title
        context['button_type'] = self.button_type
        context['basic_url'] = self.basic_url
        context['advanced_url'] = self.advanced_url
        context['buttons'] = self.buttons
        return context

    def post(self, request, *args, **kwargs): #handles all posts

        # updates number of records to be handled for "Update" button
        if "quantity" in self.request.POST:
            self.object = None
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


class GenericUpdateFormSet(UpdateView):
    # class defaults
    initial_data = []
    extra = 0
    upload_form = UploadFileForm()
    pks = None
    formset = None

    def get_formset(self): #makes formset for various defs within class
        formset = modelformset_factory(
            self.model,
            form=self.form_class,
            fields=self.field,
            extra=self.extra
        )
        return formset

    def get_context_data(self, *args, **kwargs): #gets context for building formset
        context = super().get_context_data(**kwargs)

        if not self.formset:
            formset = self.get_formset()
            if self.pks is None:
                queryset = self.model.objects.none()
            else:
                queryset = self.model.objects.filter(pk__in=self.pks)
            context['formset'] = formset(queryset=queryset, initial=self.initial_data)
        else:
            context['formset'] = self.formset

        context['title'] = self.title
        context['button_type'] = self.button_type
        context['basic_url'] = self.basic_url
        context['advanced_url'] = self.advanced_url
        context['buttons'] = self.buttons
        return context

    def get(self, request, *args, **kwargs): #handles all gets
        self.object = None
        context = self.get_context_data()
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs): #handles all posts
        # updates number of records to be handled for "Update" button
        # TODO make pks into def get_objects()
        pks = request.POST.getlist("selection")
        self.pks = pks

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

            # header
            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)

            # body
            formset = self.get_formset()
            formset_f = formset(request.POST)
            if formset_f.is_valid():
                for f in formset_f:
                    row_num += 1
                    if f.is_valid():
                        for col_num in range(len(columns)):
                            ws.write(row_num, col_num, f.cleaned_data[columns[col_num]], font_style)
                    else:
                        print('invalid')
            else:
                print('formset is invalid')

            wb.save(response)
            return response

        # uploads form and handles errors through "Choose File" and "Upload" button
        # https://django-excel.readthedocs.io/en/v0.0.1/#
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

        # saves formset
        if "save_btn" in self.request.POST:
            formset = self.get_formset()
            formset = formset(request.POST)
            if formset.is_valid():
                record_num = int(0)
                record_add = int(0)
                for form in formset:
                    record_num += 1
                    #TODO need to make validation more DRY - move to seperate def
                    #TODO need to prevent duplicate records and ensure unique naming system
                    data = form.cleaned_data
                    if form.is_valid():
                        if form.cleaned_data == {}: # handles warning if no records
                            messages.warning(request,
                                             'Record #%d did not add because required data was missing.' % record_num)
                        elif data['id'] == None: #updates or creates uploaded records
                            record_add += 1
                            del data['id']
                            self.model.objects.update_or_create(sample_name=form.cleaned_data['sample_name'], defaults=data, )

                        else: # saves records edited in html GUI
                            record_add += 1
                            form.save()
                    else:
                        messages.warning(request, 'Form Error')
                messages.success(request, '%d records updated successfully.' % record_add)
                return HttpResponseRedirect(self.success_url)
            else:
                messages.warning(request, 'Formset Error')
                return self.render_to_response(self.get_context_data(formset=formset))

        elif pks: # handles posts from browser when pks are present
            self.object = None
            context = self.get_context_data()
            return render(request, self.template_name, context=context)

        else:
            self.object = None
            formset = self.get_formset()
            formset = formset(request.POST)
            print(formset)
            pks = []
            for form in formset:
                pks += self.model.objects.filter(sample_name=form.cleaned_data['sample_name']).values_list('pk', flat=True)
                self.pks = pks
            context = self.get_context_data()
            return render(request, self.template_name, context=context)
