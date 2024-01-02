from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from .forms import UploadFileForm
from utils.uploadings import handle_uploaded_file


def download_data(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            if handle_uploaded_file(form.cleaned_data['file']):
                return HttpResponse('File uploaded')
            else:
                return HttpResponse('File has no json format')
    else:
        form = UploadFileForm()
        # if uploading_file:
        #     messages.success(request, 'Успешная загрузка')
        # else:
        #     messages.error(request, 'Ошибка при загрузке')
    return render(request, 'download_data.html', context={'title': 'Load file', 'form': form})


def show_data(request):
    return render(request, 'show_data.html', context={'title': 'Show data'})