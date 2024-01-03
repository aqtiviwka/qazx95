import os

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import UploadFileForm
from load_json_file.models import Data
import json
from re import fullmatch


def download_data(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            return handle_uploaded_file(form.cleaned_data['file'])
    else:
        form = UploadFileForm()
    return render(request, 'download_data.html', context={'title': 'Load file', 'form': form})


def show_data(request):
    data_list = Data.objects.all()
    return render(request, 'show_data.html', context={'title': 'Show data', 'data_list': data_list})


def error_of_format_file(request):
    return render(request, 'error_of_format_file.html', context={'title': 'Error of format file'})


def error_of_format_data(request):
    return render(request, 'error_of_format_data.html', context={'title': 'Error of format data'})


def error_of_keys(request):
    return render(request, 'error_of_keys.html', context={'title': 'Error of keys'})


def everything_is_correct(request):
    return render(request, 'everything_is_correct.html', context={'title': 'everything_is_correct'})


def handle_uploaded_file(f):
    with open(f"uploads/{f.name}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
        print('Файл загружен')
    if f.name[-5:] == '.json':
        with open(f"uploads/{f.name}", "r") as json_file:
            data = json.load(json_file)
            dict_data = []
        os.remove(f"uploads/{f.name}")
        print('Файл удален')
        if all(map(lambda item: ('name' in item) and ('date' in item), data)):
            print('File is correct')
            for d in data:
                if len(d['name']) >= 50 or not fullmatch('[0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{2}:[0-9]{2}', d['date']):
                    print('Data is not valid')
                    dict_data = []
                    return redirect(error_of_format_data)
                else:
                    dict_data.append(dict(name=d["name"], date=d["date"].replace('_', ' ')))
            print(dict_data)
            if dict_data:
                for note in dict_data:
                    d1 = Data.objects.create(name=note['name'], date=note['date'])
                    d1.save()

        else:
            return redirect(error_of_keys)
        return redirect(everything_is_correct)
    else:
        os.remove(f"uploads/{f.name}")
        print('Файл удален')
        return redirect(error_of_format_file)