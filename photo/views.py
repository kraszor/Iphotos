from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView

from .forms import CreateGroupForm
from .models import UsersGroup


def home(request):
    return render(request, 'photo/home.html', {})


def download(request):
    return render(request, 'photo/download.html', {})


def export(request):
    filename = "test.zip" # this is the file people must download
    with open(filename, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=' + filename
        response['Content-Type'] = 'application/zip; charset=utf-16'
        return response


class GroupCreate(CreateView):
    model = UsersGroup
    form_class = CreateGroupForm
    # fields = ['name', 'description', 'users']
