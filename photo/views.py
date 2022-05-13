from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .forms import CreateGroupForm
from .models import UsersGroup, Place, Image, Photo
from .serializers import UsersGroupSerializer,\
                         PlaceSerializer, \
                         ImageSerializer,\
                         PhotoSerializer


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

# SERIALIZERS FOR API


@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'Groups': '/api/groups',
        'Places': '/api/places',
        'Images': '/api/images',
        'Photos': '/api/photos',
        'Detail of group': '/api/groups/<int:pk>',
    }
    return Response(api_urls)

@api_view(['GET', 'POST'])
def groups_list(request):
    if request.method == 'GET':
        groups = UsersGroup.objects.all()
        serializer = UsersGroupSerializer(groups, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UsersGroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def places_list(request):
    if request.method == 'GET':
        places = Place.objects.all()
        serializer = PlaceSerializer(places, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PlaceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def images_list(request):
    if request.method == 'GET':
        images = Image.objects.all()
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def photos_list(request):
    if request.method == 'GET':
        photos = Photo.objects.all()
        serializer = PhotoSerializer(photos, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def group_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        group = UsersGroup.objects.get(pk=pk)
    except UsersGroup.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UsersGroupSerializer(group)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UsersGroupSerializer(group, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)