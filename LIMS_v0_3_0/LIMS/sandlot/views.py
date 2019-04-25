from .models import Author
from .tables import AuthorTable
from .filters import AuthorListFilter
from .forms import AuthorListFormHelper
from .utils import PagedFilteredTableView

class AuthorTableList(PagedFilteredTableView):
    template_name = 'sandlot_list.html'
    model = Author
    table_class = AuthorTable
    filter_class = AuthorListFilter
    formhelper_class = AuthorListFormHelper

