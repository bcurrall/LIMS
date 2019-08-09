from sample.models import Sample
from django.shortcuts import render
from .models import Author
from .tables import AuthorTable, SampleTable, SampleTableBasic
from .filters import AuthorListFilter, SampleListFilter
from .forms import AuthorListFormHelper, SampleListFormHelper
from .utils import PagedFilteredTableView

class AuthorTableList(PagedFilteredTableView):
    template_name = 'sandlot_list.html'
    model = Author
    table_class = AuthorTable
    filter_class = AuthorListFilter
    formhelper_class = AuthorListFormHelper

    def post(self, request, *args, **kwargs):
        print("==============POST=================")
        print(request.POST)
        return render(request, self.template_name)


class SampleTableList(PagedFilteredTableView):
    template_name = 'sandlot_list.html'
    model = Sample
    table_class = SampleTableBasic
    filter_class = SampleListFilter
    formhelper_class = SampleListFormHelper

