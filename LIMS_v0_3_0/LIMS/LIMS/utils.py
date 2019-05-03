from django_tables2 import SingleTableView

class PagedFilteredTableView(SingleTableView): # generic filter and get_context for table + filter views
    filter_class = None
    formhelper_class = None
    context_filter_name = 'filter'
    title = None
    button_type = None
    buttons = None

    def get_queryset(self, **kwargs):
        qs = super(PagedFilteredTableView, self).get_queryset()
        self.filter = self.filter_class(self.request.GET, queryset=qs)
        self.filter.helper = self.formhelper_class()
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super(PagedFilteredTableView, self).get_context_data()
        context[self.context_filter_name] = self.filter
        context['title'] = self.title
        context['button_type'] = self.button_type
        context['buttons'] = self.buttons
        return context