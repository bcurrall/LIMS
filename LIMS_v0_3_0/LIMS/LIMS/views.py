# this views in LIMS app is only for generic views
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView, UpdateView
from django.forms import modelformset_factory
from django.contrib import messages
from django.core.exceptions import ValidationError
from django_tables2 import SingleTableView
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404

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
class PagedFilteredTableView(SingleTableView):
    '''
    generic filter and get_context for table + filter views
    '''
    print('=============PagedFilteredTableView=====================')
    filter_class = None
    formhelper_class = None
    context_filter_name = 'filter'
    title = None
    button_type = None
    buttons = None
    buttons_processing_type = None
    buttons_processing = None
    qs = None


    def get_buttons(self):
        '''
        custom function to get and update buttons from instances
        updates button class based on page instance
        '''
        # TODO not DRY same function used in GenericUpdateFormSet
        # TODO setup buttons so that None is an option
        buttons = self.buttons
        page = self.page
        for button in buttons:
            if button['name'] == page:
                button['class'] = 'btn btn-success'
            else:
                button['class'] = 'btn btn-default'
        return buttons

    def get_queryset(self, **kwargs):
        '''
        updates django get_queryset
        gets qs and filters with the filter.helpers
        '''
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
        '''
        updates django get_context_data
        gets html context based on filters
        integrates all custom context variables
        '''
        print('=======get_context_data===================')
        context = super(PagedFilteredTableView, self).get_context_data()
        context[self.context_filter_name] = self.filter
        context['title'] = self.title
        context['button_type'] = self.button_type
        context['buttons'] = self.get_buttons()
        context['buttons_processing_type'] = self.buttons_processing_type
        context['buttons_processing'] = self.buttons_processing
        return context

    def get(self, request, *args, **kwargs):
        '''
        updates django get function
        integrates the PagedFilteredTableView parameters
        '''
        print('============GET=======================')
        self.query = request.GET
        response = super(PagedFilteredTableView, self).get(request)
        return response

    def post(self, request, *args, **kwargs):  # handles all posts
        '''
        highly custom post (does not update django function)
        handles btn clicks to and from this view
        '''
        # universal POST variable - defines universal variables pks, qs and query
        # TODO figure out if/should be integrated to django base post
        print('===========POST==================')
        pks = request.POST.getlist("selection")
        self.qs = self.model.objects.filter(pk__in=pks)
        self.query = request.GET # TODO why GET here?

        if "del_btn" in request.POST:
            print('===========del_btn==================')
            # creates warning in nothing selected
            if pks:
                pass
            else:
                self.qs = 'Empty'
                messages.warning(request, 'Nothing selected.')

        elif "del_confirm_btn" in request.POST:
            # deletes, counts and creates warning for all selections
            print('===========del_confirm_btn==================')
            num_deleted = len(pks)
            self.qs.delete()
            self.qs = None
            messages.warning(request, '%d samples deleted.' %num_deleted)

        elif "cancel_btn" in request.POST:
            # creates warning that nothing is deleted
            messages.success(request, 'No records were deleted.')

        else:
            # TODO handle else errors
            pass

        # loads page with all or just selection
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

    def get_buttons(self):
        # TODO setup buttons so that None is an option
        buttons = self.buttons
        page = self.page
        for button in buttons:
            if button['name'] == page:
                button['class'] = 'btn btn-success'
            else:
                button['class'] = 'btn btn-default'
        return buttons

    def get_form_class_and_model(self, form_type):
        if form_type == 'current':
            form_class = self.form_classes['form_current']
            model = self.form_classes['model_current']
        elif form_type == 'parent':
            form_class = self.form_classes['form_parent']
            model = self.form_classes['model_parent']
        elif form_type == 'related':
            form_class = self.form_classes['form_related']
            model = self.form_classes['model_related']
        else:
            form_class = self.form_class
        self.form_class = form_class
        form = form_class
        return form, model

    def get_batch_id(self):
        print('=================get_batch_id====================')
        prefix = self.batch_prefix
        # prefix = 'plt'
        t = datetime.date.today()
        date = t.strftime("%Y%m%d")
        print(self.model)
        last_id = self.model.objects.filter(batch_id__icontains=date).values_list('batch_id', flat=True).last()
        if last_id:
            postfix = '{0:0=3d}'.format(int(last_id.split('_')[-1]) + 1)
        else:
            postfix = '{0:0=3d}'.format(1)
        batch_id = prefix + date + '_' + postfix
        print(batch_id)
        return batch_id

    def get_pks(self):
        # TODO this is a dangerous as may not flow the way intended, figure out how to better generalize
        if self.pks:
            pks = self.pks
        elif self.parent_pks:
            parent_pks = self.parent_pks
            parent_pk = parent_pks[0]
            pks = self.model.objects.filter(parent_name=parent_pk).values_list('pk', flat=True)
        else:
            pks = None
        return pks

    def create_pks(self):
        print('=============create_pks===============')
        objects = []
        self.get_batch_id()
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
            self.model = self.form_classes['model_current']
        else:
            form_class = self.form_class

        print('=========formset variables================')
        print(form_class)
        print(self.field)
        print(self.extra)

        formset = modelformset_factory(
            self.model,
            form=form_class,
            fields=self.field,
            extra=self.extra
        )
        print(formset)
        print(self.model)
        return formset

    def get_queryset(self):
        print('==========get_queryset================')
        print(self.pks)

        if self.pks:
            print('===========self.pks============')
            queryset = self.model.objects.filter(pk__in=self.pks)

        elif self.parent_pks:
            print('===========elif self.parent_pks============')
            objects = []
            batch_id = self.get_batch_id()

            if len(self.parent_pks) < 1:
                self.extras = 5

            else:
                print('======================get_queryset else====================')
                name_num = 0
                self.extras = 0
                for parent_pk in self.parent_pks:
                    name_num += 1
                    print(name_num)
                    pk = self.model_parent.objects.get(pk=parent_pk)
                    prefix = self.record_prefix
                    lib_name = prefix + "{0:0=3d}".format(name_num)
                    object = self.model.objects.create(parent_name=pk, name=lib_name, batch_id=batch_id) #saves records and gets object id
                    objects.append(object.pk)
            queryset = self.model.objects.filter(pk__in=objects) # recalls object id

        else:
            queryset = self.model.objects.none()
        return queryset

    def get_context_data(self, *args, **kwargs): #gets context for building formset
        # should call get_form_class_and_model and set form_class before super
        context = super().get_context_data(**kwargs)

        if self.form_classes: #get parent form with or without object
            print('=============if form_p in self.form_classes:================')
            form_p = self.form_classes['form_parent']
            model_p = self.form_classes['model_parent']
            parent_pks = self.parent_pks
            if parent_pks:
                parent_pk = parent_pks[0]
                form_p = form_p(instance=model_p.objects.get(pk=parent_pk))
            else:
                parent_pk = None
            print(parent_pks)
            print(parent_pk)
            # form_p = form_p(instance=model_p.objects.get(pk=parent_pk))
            context['form_p'] = form_p
        else:
            print('===========else of self.form_class=================')
            context['form_p'] = []

        formset = self.get_formset()
        queryset = self.get_queryset()
        print(formset)
        print(queryset)
        context['formset'] = formset(queryset=queryset, initial=self.initial_data)
        context['title'] = self.title
        context['button_type'] = self.button_type
        context['buttons'] = self.get_buttons()
        context['buttons_processing_type'] = self.buttons_processing_type
        context['buttons_processing'] = self.buttons_processing
        return context

    def form_save_with_msgs(self, form, request, record_num, record_add):
        print('===========def form_save_with_msgs_render==============')
        print(form.cleaned_data)
        record_ids = []
        if form.cleaned_data == {}:  # handles warning if no records
            print('=====form.cleaned_data == {}=============================')
            messages.warning(request,
                             'Record #%d did not add because required data was missing.' % record_num)
        elif form.cleaned_data.get('id') == None:  # checks ids to see if object is loaded - missing after upload
            print('=====form.cleaned_data.get(id) == None =============================')
            record_add += 1
            try:
                del form.cleaned_data['id']
            except KeyError:
                pass
            if form.cleaned_data.get('unique_id') == None:  # if unique id is not present then new record
                print('===============unique_id == None =====================')
                record = form.save()
                record_ids.append(record.id)
            else:  # reloads obj based on unique_id, protects parent_name, but allows updating of uploaded info
                # TODO consider scenarios where "_or_create" would be necessary (i.e., can it just be "update")
                print('===============else==================')
                try:
                    form.cleaned_data['parent_name']
                    print(form.cleaned_data['parent_name'])
                    if form.cleaned_data['parent_name']:
                        self.model.objects.update_or_create(unique_id=form.cleaned_data['unique_id'],
                                                            defaults=form.cleaned_data, )
                        record_ids.append(self.model.objects.filter(unique_id=form.cleaned_data['unique_id']).values_list('pk', flat=True).first())
                    else:
                        del form.cleaned_data['parent_name']  # prevents from overwritting parent
                        self.model.objects.update_or_create(unique_id=form.cleaned_data['unique_id'],
                                                            defaults=form.cleaned_data, )
                        record_ids.append(self.model.objects.filter(unique_id=form.cleaned_data['unique_id']).values_list('pk', flat=True).first())
                except KeyError:  # occurs when uploading data without parent_name key
                    self.model.objects.update_or_create(unique_id=form.cleaned_data['unique_id'],
                                                        defaults=form.cleaned_data, )
                    record_ids.append(self.model.objects.filter(unique_id=form.cleaned_data['unique_id']).values_list('pk', flat=True).first())
        else:  # saves records edited directly in html GUI
            print('=====else=============================')
            record_add += 1
            record = form.save()
            record_ids.append(record.id)
        print('=============records_ids================')
        print(record_ids)
        return form, request, record_ids, record_num, record_add

    def get(self, request, *args, **kwargs): #handles all gets
        print('===========get================')
        self.object = None
        context = self.get_context_data()
        print(self.pks)
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs): #handles all posts
        # TODO make pks into def get_objects()
        # TODO would this get_formset be better distributed to each POST def
        print('===============POST======================')
        formset = self.get_formset() # gets empty formset

        try: #checks to see if any post fills empty formset
            # checks to see if a formset if posted and either keeps formset (try - swithching fields) or sets it equal to None (except - coming from browser)
            formset = formset(request.POST)
            self.formset = formset
            # TODO replace print with some other way to catch "Management" error
            print(formset.cleaned_data)
        except (ValidationError, AttributeError):
            formset = None
            self.formset = formset

        if "export_btn" in request.POST:
            # exports file based on formset through "Export" button
            # from https://simpleisbetterthancomplex.com/tutorial/2016/07/29/how-to-export-to-excel.html
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

        elif "upload_btn" in request.POST:
            # uploads form and handles errors through "Choose File" and "Upload" button
            # https://django-excel.readthedocs.io/en/v0.0.1/#
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


        elif "save_btn" in self.request.POST:
            # saves formset
            print('==============save_btn=====================')
            if formset.is_valid():
                record_num = int(0)
                record_add = int(0)
                for form in formset:
                    record_num += 1
                    if form.is_valid():
                        form, request, record_ids, record_num, record_add = self.form_save_with_msgs(form, request, record_num, record_add)
                    else:
                        messages.warning(request, 'Form Error')
                messages.success(request, '%d records updated successfully.' % record_add)
                return HttpResponseRedirect(self.success_url)
            else:
                messages.warning(request, 'Formset Error')
                return self.render_to_response(self.get_context_data(formset=formset))

        elif "save_form_btn" in self.request.POST:
            print('===========save_form_btn====================')
            self.object = None
            # form_class = PoolForm
            form_type = 'parent'
            form, model = self.get_form_class_and_model(form_type)
            form_class = form
            form = form(request.POST)
            # self.form_classes('model_parent')
            self.model = model
            record_num = 1
            record_add = int(0)
            if form.is_valid():
                form, request, record_ids, record_num, record_add = self.form_save_with_msgs(form, request, record_num, record_add)
            else:
                messages.warning(request, 'Form Error')
            # self.success_url = reverse_lazy('library:pooling')
            print('===============selection================')
            self.selection = record_ids
            print(self.selection)
            self.parent_pks = self.selection
            messages.success(request, '%d records updated successfully.' % record_add)
            # return HttpResponseRedirect(self.success_url)
            # return redirect('library:pooling')
            form_type = 'current'
            form, model = self.get_form_class_and_model(form_type)
            self.model = model
            pks = self.get_pks()
            self.pks = pks
            context = self.get_context_data()
            return render(request, self.template_name, context=context)

        elif "update_2_form_btn" in self.request.POST: #handles updating of 2 form views
            print('===========elif "update_2_form_btn" in self.request.POST=========')
            self.object = None
            parent_pks = request.POST.getlist("selection")
            if len(parent_pks) > 1:
                messages.warning(request, 'Only first record chosen can be displayed')
                self.parent_pks = parent_pks
            elif len(parent_pks) < 1:
                self.parent_pks = self.selection
            else:
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
            # make parentname and parent object
            # make childname and child objects -> link to parent (i.e., pool)
            # get context (same as update_2_form_btn)

            self.object = None
            # make parent data
            obj = []
            form_type = 'parent'
            form_p, model_p = self.get_form_class_and_model(form_type)
            form_type = 'related'
            form_r, model_r = self.get_form_class_and_model(form_type)
            form_type = 'current'
            form_c, model_c = self.get_form_class_and_model(form_type)
            self.model = model_p
            batch_id = self.get_batch_id()
            print(batch_id)
            parent = model_p.objects.create(batch_id=batch_id)
            print(model_p)
            print(parent)
            print(parent.pk)
            obj.append(parent.pk)
            print(obj)
            self.parent_pks = obj
            print(self.parent_pks)
            pks = request.POST.getlist("selection")
            objs = []
            print(pks)
            for pk in pks:
                print(self.model)
                related = model_r.objects.get(pk=pk)
                print('=============library=============')
                print(related)
                child = model_c.objects.create(related_name=related, parent_name=parent)
                objs.append(child.pk)
            print(objs)
            self.pks = objs
            print(self.pks)

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

        elif "generate_btn" in self.request.POST:
            self.object = None
            '''
            pseudo code:
            gets the method dependent function/variables
            '''
            print('===========POST get_lanes_btn=========')
            request, parent_pk, pks, test = self.get_lanes(request)
            print(test)
            print(parent_pk)
            print('pks = %s' % pks)
            self.pks = pks
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
            print('============POST elif formset is not None=============')
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
            print('============POST else=============')
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
