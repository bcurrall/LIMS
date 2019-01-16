from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# landing page for entire website
def index(request):
    return render(request, 'home/index.html')


