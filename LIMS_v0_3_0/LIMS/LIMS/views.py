# this views in LIMS app is only for generic views
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView, UpdateView
from django.forms import modelformset_factory
from django.contrib import messages
from django.core.exceptions import ValidationError
from django_tables2 import SingleTableView

from .forms import UploadFileForm
from sample.models import Sample
from library.models import Library, PoolingAmount
from library.forms import PoolForm

import xlwt
import datetime
import csv
# time stamp
now = datetime.datetime.now()
date_stamp = now.strftime("%d%m%Y")


# Browser/List Master View
class PagedFilteredTableView(SingleTableView): # generic filter and get_context for table + filter views
    filter_class = None
    formhelper_class = None
    context_filter_name = 'filter'
    title = None
    button_type = None
    buttons = None
    qs = None
    print('=============PagedFilteredTableView=====================')

    def get_buttons(self):
        buttons = self.buttons
        page = self.page
        for button in buttons:
            if button['name'] == page:
                button['class'] = 'btn btn-success'
            else:
                button['class'] = 'btn btn-default'
        return buttons

    def get_queryset(self, **kwargs):
        print('===========get_queryset=============')
        if self.qs:
            if self.qs == 'Empty':
                qs = self.model.objects.none()
            else:
                qs = self.qs
        else:
            qs = super(PagedFilteredTableView, self).get_queryset()
        self.filter = self.filter_class(self.query, queryset=qs)
        self.filter.helper = self.formhelper_class()
        return self.filter.qs

    def get_context_data(self, **kwargs):
        print('=======get_context_data===================')
        context = super(PagedFilteredTableView, self).get_context_data()
        context[self.context_filter_name] = self.filter
        context['title'] = self.title
        context['button_type'] = self.button_type
        context['buttons'] = self.get_buttons()
        return context


    def get(self, request, *args, **kwargs):
        print('============GET=======================')
        self.query = request.GET
        response = super(PagedFilteredTableView, self).get(request)
        return response


    def post(self, request, *args, **kwargs):  # handles all posts
        print('===========POST==================')
        pks = request.POST.getlist("selection")
        print(pks)
        print(self.model)
        self.qs = self.model.objects.filter(pk__in=pks)
        print(self.qs)
        self.query = request.GET

        if "del_btn" in request.POST:
            if pks:
                pass
            else:
                self.qs = 'Empty'
                messages.warning(request, 'Nothing selected.')

        if "del_confirm_btn" in request.POST:
            print('===========del_confirm_btn==================')
            num_deleted = len(pks)
            print(self.qs)
            self.qs.delete()
            self.qs = None
            messages.warning(request, '%d samples deleted.' %num_deleted)
        if "cancel_btn" in request.POST:
            messages.success(request, 'No records were deleted.')

        response = super(PagedFilteredTableView, self).get(request)
        return response


# Create/Update Master View
class GenericUpdateFormSet(UpdateView):
    # class defaults
    initial_data = []
    extra = 0
    upload_form = UploadFileForm()
    pks = None
    parent_pks = None
    formset = None
    form_p = None
    form_classes = None

    def get_form_class_and_model(self, form_type):
        if form_type == 'current':
            form_class = self.form_classes['form_current']
            model = self.form_classes['model_current']
        elif form_type == 'parent':
            form_class = self.form_classes['form_parent']
            model = self.form_classes['model_parent']
        else:
            form_class = self.form_class
        self.form_class = form_class
        form = form_class
        return form, model

    def get_pks(self):
        if self.pks:
            pks = self.pks
        elif self.parent_pks:
            parent_pks = self.parent_pks
            parent_pk = parent_pks[0]
            pks = self.model.objects.filter(pool_name=parent_pk).values_list('pk', flat=True)
        else:
            pks = None
        return pks

    def create_pks(self):
        objects = []
        if len(self.parent_pks) < 1:
            self.extras = 5
            pks = None

        else:
            name_num = 0
            self.extras = 0
            for parent_pk in self.parent_pks:
                name_num += 1
                print(name_num)
                pk = self.model_parent.objects.get(pk=parent_pk)
                lib_name = 'lib' + "{0:0=3d}".format(name_num)
                self.model.objects.create(parent_name=pk, name=lib_name)
                objects.append(lib_name)
            pks = self.model.objects.filter(name__in=objects).values_list('pk', flat=True)
        return pks

    def get_formset(self): #makes formset for various defs within class
        print('========get_formset=================')

        if self.form_classes: #gets form_class from form_classes or form_class
            form_class = self.form_classes['form_current']
            model = self.form_classes['form_current']
        else:
            form_class = self.form_class

        print(self.model)
        print(form_class)
        print(self.field)
        print(self.extra)
        formset = modelformset_factory(
            self.model,
            form=form_class,
            fields=self.field,
            extra=self.extra
        )
        return formset

    def get_queryset(self):
        print('==========get_queryset================')
        print(self.pks)
        if self.pks:
            queryset = self.model.objects.filter(pk__in=self.pks)

        elif self.parent_pks:
            objects = []

            if len(self.parent_pks) < 1:
                self.extras = 5

            else:
                name_num = 0
                self.extras = 0
                for parent_pk in self.parent_pks:
                    name_num += 1
                    print(name_num)
                    pk = self.model_parent.objects.get(pk=parent_pk)
                    lib_name = 'lib' + "{0:0=3d}".format(name_num)
                    object = self.model.objects.create(parent_name=pk, name=lib_name) #saves records and gets object id
                    objects.append(object.pk)
            queryset = self.model.objects.filter(pk__in=objects) # recalls object id

        else:
            queryset = self.model.objects.none()
        return queryset

    def get_context_data(self, *args, **kwargs): #gets context for building formset
        context = super().get_context_data(**kwargs)

        if self.form_classes: #get parent form with or without object
            form_p = self.form_classes['form_parent']
            parent_pks = self.parent_pks
            parent_pk = parent_pks[0]
            print('=============if form_p in self.form_classes:================')
            print(parent_pks)
            print(parent_pk)
            form_p = form_p(instance=self.model_parent.objects.get(pk=parent_pk))
            context['form_p'] = form_p
        else:
            print('===========else of self.form_class=================')
            context['form_p'] = []

        formset = self.get_formset()
        queryset = self.get_queryset()
        # context['form_p'] = form_p
        context['formset'] = formset(queryset=queryset, initial=self.initial_data)
        context['title'] = self.title
        context['button_type'] = self.button_type
        context['buttons'] = self.get_buttons()
        return context

    def form_save_with_msgs(self, form, request, record_num, record_add):
        print('===========def get_msg_save_render==============')
        print(form.cleaned_data)
        if form.cleaned_data == {}:  # handles warning if no records
            print('=====form.cleaned_data == {}=============================')
            messages.warning(request,
                             'Record #%d did not add because required data was missing.' % record_num)
        elif form.cleaned_data.get('id') == None:  # checks ids to see if object is loaded - missing after upload
            print('=====form.cleaned_data.get(id)=============================')
            record_add += 1
            try:
                del form.cleaned_data['id']
            except KeyError:
                pass
            if form.cleaned_data.get('unique_id') == None:  # if unique id is not present then new record
                form.save()
            else:  # reloads obj based on unique_id, protects parent_name, but allows updating of uploaded info
                # TODO consider scenarios where "_or_create" would be necessary (i.e., can it just be "update")
                try:
                    form.cleaned_data['parent_name']
                    if form.cleaned_data['parent_name']:
                        self.model.objects.update_or_create(unique_id=form.cleaned_data['unique_id'],
                                                            defaults=form.cleaned_data, )
                    else:
                        del form.cleaned_data['parent_name']  # prevents from overwritting parent
                        self.model.objects.update_or_create(unique_id=form.cleaned_data['unique_id'],
                                                            defaults=form.cleaned_data, )
                except KeyError:  # occurs when uploading data without parent_name key
                    self.model.objects.update_or_create(unique_id=form.cleaned_data['unique_id'],
                                                        defaults=form.cleaned_data, )
        else:  # saves records edited directly in html GUI
            print('=====else=============================')
            record_add += 1
            form.save()
        return form, request, record_num, record_add

    def get(self, request, *args, **kwargs): #handles all gets
        print('===========get================')
        self.object = None
        context = self.get_context_data()
        print(self.pks)
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs): #handles all posts
        # TODO make pks into def get_objects()
        print('===============POST======================')
        formset = self.get_formset() # gets empty formset
        print(formset)
        # print(formset())

        #checks to see if a formset if posted and either keeps formset (try - swithching fields) or sets it equal to None (except - coming from browser)
        try: #checks to see if any post fills empty formset
            formset = formset(request.POST)
            self.formset = formset
            # TODO replace print with some other way to catch "Management" error
            print(formset.cleaned_data)
        except ValidationError:
            formset = None
            self.formset = formset

        # exports file based on formset through "Export" button
        # from https://simpleisbetterthancomplex.com/tutorial/2016/07/29/how-to-export-to-excel.html
        if "export_btn" in request.POST:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="form_export.csv"'
            writer = csv.writer(response)

            #header
            writer.writerow(self.field)
            columns = self.field

            #rows
            row_num = 0
            if formset.is_valid():
                for form in formset:
                    row_num += 1
                    if form.is_valid():
                        row = []
                        for column in columns:
                            value = form.cleaned_data.get(column) #internal note: not sure why .get instead of just ['column']
                            row.append(value)
                        writer.writerow(row)
                    else:
                        print('invalid')
            else:
                print('formset is invalid')
            return response

        # uploads form and handles errors through "Choose File" and "Upload" button
        # https://django-excel.readthedocs.io/en/v0.0.1/#
        if "upload_btn" in request.POST:
            upload_form = UploadFileForm(request.POST, request.FILES)
            #handle pks and formatting (e.g., boolean when uploading
            if upload_form.is_valid():
                filehandle = request.FILES['myfile']
                initial_data = filehandle.get_records()
                self.initial_data = initial_data
                self.object = None
                extra = 0
                for record in initial_data:
                     extra = extra + 1
                self.extra = extra
                context = self.get_context_data()
                return render(request, self.template_name, context=context)
            # TODO unhandled exception form_invalid

        # saves formset
        if "save_btn" in self.request.POST:
            if formset.is_valid():
                record_num = int(0)
                record_add = int(0)
                for form in formset:
                    record_num += 1
                    if form.is_valid():
                        form, request, record_num, record_add = self.form_save_with_msgs(form, request, record_num, record_add)
                    else:
                        messages.warning(request, 'Form Error')
                messages.success(request, '%d records updated successfully.' % record_add)
                return HttpResponseRedirect(self.success_url)
            else:
                messages.warning(request, 'Formset Error')
                return self.render_to_response(self.get_context_data(formset=formset))

        elif "save_form_btn" in self.request.POST:
            print('===========save_form_btn====================')
            form_class = PoolForm
            form_type = 'parent'
            form, model = self.get_form_class_and_model(form_type)
            form = form(request.POST)
            # self.form_classes('model_parent')
            self.model = model
            record_num = 1
            record_add = int(0)
            if form.is_valid():
                form, request, record_num, record_add = self.form_save_with_msgs(form, request, record_num, record_add)
            else:
                messages.warning(request, 'Form Error')
            messages.success(request, '%d records updated successfully.' % record_add)
            return HttpResponseRedirect(self.success_url)

        elif "update_2_form_btn" in self.request.POST: #handles updating of 2 form views
            print('===========elif "update_2_form_btn" in self.request.POST=========')
            self.object = None
            parent_pks = request.POST.getlist("selection")
            if len(parent_pks) > 1:
                messages.warning(request, 'Only first record chosen can be displayed')
            self.parent_pks = parent_pks
            pks = self.get_pks()
            self.pks = pks
            form_type = 'current'
            form, model = self.get_form_class_and_model(form_type)
            context = self.get_context_data()
            return render(request, self.template_name, context=context)

        # captures ids to use in processing
        elif "process_2_form_btn" in self.request.POST: #handles processing and saving of new records derived from parent record in 1-to-1 relationship
            print('===================process_2_form_btn===============')
            ### pseudocode
            # make poolname and pool object
            # make poolamountname and poolamount objects -> link to parent (i.e., pool)
            # get context (same as update_2_form_btn)

            self.object = None
            # make parent data
            obj = []
            form_type = 'parent'
            form, model = self.get_form_class_and_model(form_type)
            pool_name_sm = 'pool_' + str(date_stamp)
            num_results = model.objects.filter(name__contains=pool_name_sm).count()
            pool_name = pool_name_sm + '_0' + str(num_results + 1)
            pool = model.objects.create(name=pool_name)
            print(pool)
            print(pool.pk)
            obj.append(pool.pk)
            print(obj)
            self.parent_pks = obj
            print(self.parent_pks)
            pks = request.POST.getlist("selection")
            objs = []
            for pk in pks:
                library = Library.objects.get(pk=pk)
                print('=============library=============')
                print(library)
                poolingamount = PoolingAmount.objects.create(library_name=library, pool_name=pool)
                objs.append(poolingamount.pk)
            print(objs)
            self.pks = objs
            print(self.pks)
            form_type = 'current'
            form, model = self.get_form_class_and_model(form_type)
            context = self.get_context_data()
            return render(request, self.template_name, context=context)

        # captures ids to use in processing
        elif "process_btn" in self.request.POST: #handles processing and saving of new records derived from parent record in 1-to-1 relationship
            self.object = None
            parent_pks = request.POST.getlist("selection")
            self.parent_pks = parent_pks
            context = self.get_context_data()
            return render(request, self.template_name, context=context)

        elif "del_btn" in self.request.POST:
            pass

        elif "del_confirm_btn" in self.request.POST:
            pks = request.POST.getlist("selection")
            sample = Sample.objects.filter(pk__in=pks)
            num_deleted = len(pks)
            sample.delete()
            messages.warning(request, '%d samples deleted.' % num_deleted)
            context = self.get_context_data()
            return render(request, self.template_name, context=context)

        elif "cancel_btn" in self.request.POST:
            messages.success(request, 'No records were deleted.')
            context = self.get_context_data()
            return render(request, self.template_name, context=context)

        # captures ids coming from browser
        elif request.POST.getlist("selection"):
            self.object = None
            pks = request.POST.getlist("selection")
            self.pks = pks
            context = self.get_context_data()
            print('===========request.POST.getlist("selection")=========')
            print(self.pks)
            return render(request, self.template_name, context=context)

        # recaptures ids for switching field views
        elif formset is not None:
            self.object = None
            formset
            pks = []
            for form in formset: #gets_pks_from_form
                pks += self.model.objects.filter(unique_id=form.cleaned_data['unique_id']).values_list('pk', flat=True)
            self.pks = pks
            context = self.get_context_data()
            return render(request, self.template_name, context=context)


        # processes all empty requests
        else:
            self.object = None
            context = self.get_context_data()
            return render(request, self.template_name, context=context)


# archived views
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
        context['buttons'] = self.get_buttons()
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
            # response = HttpResponse(content_type='application/ms-excel')
            # response['Content-Disposition'] = 'attachment; filename="samples.xls"'
            # wb = xlwt.Workbook(encoding='utf-8')
            # ws = wb.add_sheet('Sample')
            # row_num = 0
            # font_style = xlwt.XFStyle()
            # font_style.font.bold = True
            # columns = self.field
            # for col_num in range(len(columns)):
            #     ws.write(row_num, col_num, columns[col_num], font_style)
            # wb.save(response)

            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="users.csv"'

            writer = csv.writer(response)
            writer.writerow(self.field)
            columns = self.field
            for column in columns:
                writer.writerow(column)
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
