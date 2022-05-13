from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

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

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    # fields = ['name', 'description', 'users']
    # template_name = 'photo/usersgroup_form.html'


class GroupsView(ListView):
    model = UsersGroup
    context_object_name = 'groups'
    # print(Film.objects.all().order_by('-release_date')[:9])

    def get_queryset(self):
        user = self.request.user
        return UsersGroup.objects.all().filter(Q(users=user) | Q(owner=user)).distinct()

    template_name = 'photo/groups.html'
