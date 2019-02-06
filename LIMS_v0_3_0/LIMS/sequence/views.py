from django.shortcuts import render
from .forms import WUSSubmissionForm


def test(request):

    form = WUSSubmissionForm

    context = {
        "form": form,
    }
    return render(request, 'sequence/test.html', context)
