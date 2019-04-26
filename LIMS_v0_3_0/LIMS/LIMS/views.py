# this views in LIMS app is only for generic views
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View, DeleteView, CreateView, FormView
from django.forms import modelformset_factory
from django.contrib import messages

from .forms import UploadFileForm

import xlwt

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
