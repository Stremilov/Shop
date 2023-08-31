from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib import messages

from .forms import UserBioForms, UploadFileForm

def process_get_view(request: HttpRequest) -> HttpResponse:
    a = request.GET.get('a', '')
    b = request.GET.get('b', '')
    result = a + b
    context = {
        'a': a,
        'b': b,
        'result': result,
    }
    return render(request, 'requestdataapp/request-query-params.html', context=context)


def user_form(request: HttpRequest) -> HttpResponse:
    context = {
        'form': UserBioForms()
    }
    return render(request, 'requestdataapp/user-bio-form.html', context=context)


def handle_file(request: HttpRequest):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            myfile = request.FILES('myfile')
            fs = FileSystemStorage()
            if fs.size('myfile') > 1048576:
                messages.error(request, 'File is too big(1 mb max).')
                render(request, 'requestdataapp/file-upload.html')
            filename = fs.save(myfile.name, myfile)
    else:
        form = UploadFileForm()
    context = {
        'form': form,
    }

    return render(request, 'requestdataapp/file-upload.html', context=context)