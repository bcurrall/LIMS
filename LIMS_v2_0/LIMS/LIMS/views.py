__author__ = "Ashok Ragavendran"
__license__ = "GPL"
__version__ = "1.0.1"
__email__ = "ashok.ragavendran@gmail.com"
__maintainer__ = "Ashok Ragavendran"
__status__ = "Production"

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from jinja2 import FileSystemLoader
from django.views.generic import TemplateView, FormView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy

from LIMS.settings import TEMPLATE_DIRS
from utils.jinja2config import environment
from .forms import NameForm, TestPage
from archive.models import Sample2

def get_name(request):
    # if this is a POST request we need to process the form data
    print("------------------------test1-------------------")
    if request.method == 'POST':
        print("------------------------test2-------------------")
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            print("------------------------test3-------------------")
            return HttpResponseRedirect('test4')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    context = {
        'form':form
    }

    return render(request, 'name.html', {'form': form})

def thanks(request):
    if request.method == "POST":
        print("------------------------test6-------------------")
    else:
        print("------------------------test7-------------------")

    return render(request, 'thanks.html', {})

def your_name(request):
    print("------------------------test8-------------------")
    if request.method == "POST":
        print("------------------------test9-------------------")
        print(request.POST.getlist('your_name'))
        name = request.POST.getlist('your_name')

    else:
        print("------------------------test10-------------------")
    return render(request, 'your-name.html', {})

def navpage(request):
    env = environment(loader=FileSystemLoader(TEMPLATE_DIRS))
    template = env.get_template('base2.html')
    return HttpResponse(template.render())

def home(request):
    return render(request, 'home.html', {})

def about(request):
    return render(request, 'about.html', {})

def base(request):
    return render(request, 'base.html', {})

## class based test page

def test(request):
    return render(request, 'test.html', {})


class TestPage(FormView):
    template_name = 'test.html'
    form_class = TestPage
    success_url = '/base/'

    def form_valid(self, form):
        return super().form_valid(form)


class SampleCreate(CreateView):
    model = Sample2
    fields = ['sample_name']


