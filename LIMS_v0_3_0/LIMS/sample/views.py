from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from LIMS.views import GenericUpdateFormSet, PagedFilteredTableView
from .models import Sample
from .forms import SampleForm, SampleListFormHelper
from .tables import SampleTableSimple, SampleTableTracking, SampleTableFull, SampleTableFreezer
from .filters import SampleListFilter
from django.contrib import messages

### Sample Browsers/FilterTables
# TODO sytalize filter maybe further to fix conflict between layout and filter parameters (e.g., exact vs. icontains)
#  SingleTableView https://stackoverflow.com/questions/25256239/how-do-i-filter-tables-with-django-generic-views
#  Also seer https://kuttler.eu/en/post/using-django-tables2-filters-crispy-forms-together/
# TODO integrate filter with number of samples per page

# Browser/Table base
class SampleTableListBase(PagedFilteredTableView):
    template_name = 'sample/selector.html'
    model = Sample
    filter_class = SampleListFilter
    formhelper_class = SampleListFormHelper
    button_type = 'buttons_1.html'
    buttons = [
        {"name": 'Simple', "class": 'btn btn-default', "url": 'sample:browser'},
        {"name": 'Tracking', "class": 'btn btn-default', "url": 'sample:browser_tracking'},
        {"name": 'Freezer', "class": 'btn btn-default', "url": 'sample:browser_freezer'},
        {"name": 'Full', "class": 'btn btn-default', "url": 'sample:browser_full'},
    ]

# Table instances
class SampleTableList(SampleTableListBase):
    title = 'Sample Browser'
    page = 'Simple'
    table_class = SampleTableSimple

class SampleTrackingTableList(SampleTableListBase):
    title = 'Tracking Browser'
    page = 'Tracking'
    table_class = SampleTableTracking

class SampleFreezerTableList(SampleTableListBase):
    title = 'Freezer Browser'
    page = 'Freezer'
    table_class = SampleTableFreezer

class SampleFullTableList(SampleTableListBase):
    title = 'Full Field Browser'
    page = 'Full'
    table_class = SampleTableFull

##### Sample CreateViews
# CreateView base (inherits from LIMS Generic CreateView)
class SampleCreateFormSetBase(GenericUpdateFormSet):
    template_name = 'sample/update.html'
    success_url = reverse_lazy('sample:browser')
    button_type = 'buttons_1.html'
    model = Sample
    form_class = SampleForm
    extra = 5
    buttons = [
        {"name": 'Basic', "class": 'btn btn-default', "url": 'sample:create'},
        {"name": 'Extract', "class": 'btn btn-default', "url": 'sample:create_extract'},
        {"name": 'Cell Line', "class": 'btn btn-default', "url": 'sample:create_cell'},
        {"name": 'Tissue', "class": 'btn btn-default', "url": 'sample:create_tissue'},
        {"name": 'Full', "class": 'btn btn-default', "url": 'sample:create_full'},
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

# CreateViews instances
class SampleCreateFormSetBasic(SampleCreateFormSetBase):
    title = 'Enter Samples Information - Basic Information'
    page = 'Basic'
    field = ('project_name','name', 'aliquot_id', 'sample_type')

class SampleCreateFormSetExtract(SampleCreateFormSetBase):
    title = 'Enter Samples Information - Extract'
    page = 'Extract'
    field = ('project_name','name','aliquot_id','sample_type','source_tissue','conc','vol', 'conc_nanodrop',
             'conc_tapestation','rin_din_tapestation','conc_qubit','species','gender','family_id','relationship','study_model','case_control','collected_by','date_collected',
             )

class SampleCreateFormSetCellLine(SampleCreateFormSetBase):
    title = 'Enter Samples Information - Full Information'
    page = 'Cell Line'
    field = ('project_name','name','aliquot_id','sample_type','source_tissue','conc','vol','weight',
             'cells','alt_name1','alt_name2','conc_nanodrop','conc_tapestation','rin_din_tapestation','conc_qubit',
             'species','gender','family_id','relationship','study_model','case_control','collected_by','date_collected',
             'collection_batch','year_of_birth','race','ethnicity','date_of_birth','strain','litter','cell_line_id',
             'passage_number','cell_line_mutation','cell_line_type','karyotype','genetic_array','other_genetic_info',
             'hpo','phenotype_desc','sample_comments','stored','freezer_name','freezer_type','freezer_shelf',
             'freezer_rack','rack_row','rack_column','box_name','box_type','aliquot_pos_row',
             'aliquot_pos_column','received','received_date','active','deactivated_date','deactivated_type',
             'tracking_comments')

class SampleCreateFormSetTissue(SampleCreateFormSetBase):
    title = 'Enter Samples Information - Human Tissues'
    page = 'Tissue'
    field = ('project_name','name','sample_type','source_tissue','weight',
             'species','gender','family_id','relationship','study_model','case_control','collected_by','date_collected',
             'collection_batch','year_of_birth','race','ethnicity','karyotype','genetic_array','other_genetic_info',
             'hpo','phenotype_desc','sample_comments')

class SampleCreateFormSetFull(SampleCreateFormSetBase):
    title = 'Enter Samples Information - Full Information'
    page = 'Full'
    field = ('project_name','name','aliquot_id','sample_type','source_tissue','conc','vol','weight',
             'cells','alt_name1','alt_name2','conc_nanodrop','conc_tapestation','rin_din_tapestation','conc_qubit',
             'species','gender','family_id','relationship','study_model','case_control','collected_by','date_collected',
             'collection_batch','year_of_birth','race','ethnicity','date_of_birth','strain','litter','cell_line_id',
             'passage_number','cell_line_mutation','cell_line_type','karyotype','genetic_array','other_genetic_info',
             'hpo','phenotype_desc','sample_comments','stored','freezer_name','freezer_type','freezer_shelf',
             'freezer_rack','rack_row','rack_column','box_name','box_type','aliquot_pos_row',
             'aliquot_pos_column','received','received_date','active','deactivated_date','deactivated_type',
             'tracking_comments')


##### Sample UpdateViews
# UpdateView Base
class SampleUpdateFormSetBase(GenericUpdateFormSet):
    template_name = 'sample/update.html'
    success_url = reverse_lazy('sample:browser')
    button_type = 'buttons_3.html'
    model = Sample
    form_class = SampleForm
    buttons = [
        {"name": 'Basic', "class": 'btn btn-success', "url": 'sample:update'},
        {"name": 'Tracking', "class": 'btn btn-default', "url": 'sample:update_tracking'},
        {"name": 'Location', "class": 'btn btn-default', "url": 'sample:update_location'},
        {"name": 'Extract', "class": 'btn btn-default', "url": 'sample:update_extract'},
        {"name": 'Cell Line', "class": 'btn btn-default', "url": 'sample:update_cell'},
        {"name": 'Tissue', "class": 'btn btn-default', "url": 'sample:update_tissue'},
        {"name": 'Full', "class": 'btn btn-default', "url": 'sample:update_full'},
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

# UpdateViews instances
class SampleUpdateFormSetBasic(SampleUpdateFormSetBase):
    title = 'Edit Samples Information - Basic Information'
    page = 'Basic'
    field = ('unique_id', 'project_name','name', 'aliquot_id', 'sample_type')

class SampleUpdateFormSetTracking(SampleUpdateFormSetBase):
    title = 'Edit Samples Information - Tracking Information'
    page = 'Tracking'
    field = ('unique_id', 'project_name', 'name', 'sample_type', 'created', 'received', 'received_date',
              'stored', 'stored_date', 'active', 'deactivated_date', 'deactivated_type', 'tracking_comments')

class SampleUpdateFormSetLocation(SampleUpdateFormSetBase):
    title = 'Edit Samples Information - Location Information'
    page = 'Location'
    field = ('unique_id', 'project_name', 'name', 'sample_type', 'received','active', 'stored', 'stored_date',
                  'freezer_name', 'freezer_type', 'freezer_shelf','freezer_rack','rack_row','rack_column',
                  'box_name', 'box_type', 'aliquot_pos_row','aliquot_pos_column', 'tracking_comments'
                  )

class SampleUpdateFormSetExtract(SampleUpdateFormSetBase):
    title = 'Edit Samples Information - Extract Information'
    page = 'Extract'
    field = ('unique_id', 'project_name','name','aliquot_id','sample_type','source_tissue','conc','vol','conc_nanodrop',
             'conc_tapestation','rin_din_tapestation','conc_qubit','species','gender','family_id','relationship','study_model',
             'case_control', 'collected_by', 'date_collected')

class SampleUpdateFormSetCellLine(SampleUpdateFormSetBase):
    title = 'Edit Samples Information - Cell Line Information'
    page = 'Cell Line'
    field = ('unique_id', 'project_name','name','aliquot_id','sample_type','source_tissue','conc','vol','weight',
             'cells','alt_name1','alt_name2','conc_nanodrop','conc_tapestation','rin_din_tapestation','conc_qubit',
             'species','gender','family_id','relationship','study_model','case_control','collected_by','date_collected',
             'collection_batch','year_of_birth','race','ethnicity','date_of_birth','strain','litter','cell_line_id',
             'passage_number','cell_line_mutation','cell_line_type','karyotype','genetic_array','other_genetic_info',
             'hpo','phenotype_desc','sample_comments','stored','freezer_name','freezer_type','freezer_shelf',
             'freezer_rack','rack_row','rack_column','box_name','box_type','aliquot_pos_row',
             'aliquot_pos_column','received','received_date','active','deactivated_date','deactivated_type',
             'tracking_comments')

class SampleUpdateFormSetTissue(SampleUpdateFormSetBase):
    title = 'Edit Samples Information - Tissue Information'
    page = 'Tissue'
    field = ('unique_id', 'project_name','name','sample_type','source_tissue','weight',
             'species','gender','family_id','relationship','study_model','case_control','collected_by','date_collected',
             'collection_batch','year_of_birth','race','ethnicity','karyotype','genetic_array','other_genetic_info',
             'hpo','phenotype_desc','sample_comments')

class SampleUpdateFormSetFull(SampleUpdateFormSetBase):
    title = 'Edit Samples Information - Full Information'
    page = 'Full'
    field = ('unique_id', 'project_name','name','aliquot_id','sample_type','source_tissue','conc','vol','weight',
             'cells','alt_name1','alt_name2','conc_nanodrop','conc_tapestation','rin_din_tapestation','conc_qubit',
             'species','gender','family_id','relationship','study_model','case_control','collected_by','date_collected',
             'collection_batch','year_of_birth','race','ethnicity','date_of_birth','strain','litter','cell_line_id',
             'passage_number','cell_line_mutation','cell_line_type','karyotype','genetic_array','other_genetic_info',
             'hpo','phenotype_desc','sample_comments','stored','freezer_name','freezer_type','freezer_shelf',
             'freezer_rack','rack_row','rack_column','box_name','box_type','aliquot_pos_row',
             'aliquot_pos_column','received','received_date','active','deactivated_date','deactivated_type',
             'tracking_comments')


### Sample DeleteView
class SampleTableListDeleteBase(PagedFilteredTableView):
    template_name = 'sample/delete.html'
    model = Sample
    filter_class = SampleListFilter
    formhelper_class = SampleListFormHelper
    # sub-class
    title = 'Are you sure you want to delete these samples?'
    page = 'Simple'
    table_class = SampleTableSimple
    button_type = 'buttons_1.html'
    buttons = []


#Archived views
def delete(request):
    title = 'Are you sure you want to delete the following samples?'
    pks = request.POST.getlist("selection")
    sample = Sample.objects.filter(pk__in=pks)
    table = SampleTableFull(Sample.objects.filter(pk__in=pks))

    if request.method == "POST":
        if "del_confirm_btn" in request.POST:
            num_deleted = len(pks)
            sample.delete()
            messages.warning(request, '%d samples deleted.' %num_deleted)
            return HttpResponseRedirect('/sample')
        if "no_btn" in request.POST:
            messages.success(request, 'No records were deleted.')
            return HttpResponseRedirect('/sample')

    context = {
        "title": title,
        "table": table,
    }
    return render(request, 'sample/delete.html', context)


