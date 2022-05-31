from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import CreateGroupForm
from .models import UsersGroup, Place, Image, Photo
from .serializers import UsersGroupSerializer, \
    PlaceSerializer, \
    ImageSerializer, \
    PhotoSerializer, LoginSerializer, UserSerializer


def home(request):
    return render(request, 'photo/home.html', {})


def download(request):
    return render(request, 'photo/download.html', {})


def export(request):
    filename = "iPhoto_x64.zip"
    with open(filename, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=' + filename
        response['Content-Type'] = 'application/zip; charset=utf-16'
        return response


class GroupCreate(LoginRequiredMixin, CreateView):
    model = UsersGroup
    form_class = CreateGroupForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class GroupsView(LoginRequiredMixin, ListView):
    model = UsersGroup
    context_object_name = 'groups'

    def get_queryset(self):
        user = self.request.user
        return UsersGroup.objects.all().filter(Q(users=user) | Q(owner=user)).distinct()

    template_name = 'photo/groups.html'


class GroupsDetail(LoginRequiredMixin, DeleteView):
    model = UsersGroup
    context_object_name = 'group'
    template_name = "photo/group_detail.html"

    def get_context_data(self, **kwargs):
        context = super(GroupsDetail, self).get_context_data(**kwargs)
        tags = self.object.tags.split('#')[1::]
        for i in range(len(tags)):
            tags[i] = '#' + tags[i]
        context['tags'] = tags
        return context


class GroupsUpdate(LoginRequiredMixin, UpdateView):
    model = UsersGroup
    form_class = CreateGroupForm
    success_url = reverse_lazy('photo:groups')


class GroupsDelete(LoginRequiredMixin, DeleteView):
    model = UsersGroup
    success_url = reverse_lazy('photo:groups')

    def get_object(self, queryset=None):
        obj = super(GroupsDelete, self).get_object()
        if not obj.owner == self.request.user:
            raise Http404
        return obj


# SERIALIZERS FOR API
@api_view(['GET'])
@permission_classes([AllowAny])
def api_overview(request):
    api_urls = {
        'Groups': '/api/groups',
        'Places': '/api/places',
        'Images': '/api/images',
        'Photos': '/api/photos',
        'Detail of the group': '/api/groups/<int:pk>',
        'Detail of the place': '/api/places/<int:pk>',
        'Detail of the image': '/api/images/<int:pk>',
        'Detail of the photo': '/api/photos/<int:pk>',
    }
    return Response(api_urls)


@api_view(['GET'])
def users_list(request):
    if request.method == 'GET':
        users = User.objects.filter(pk=request.user.id).distinct()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def groups_list(request):
    if request.method == 'GET':
        groups = UsersGroup.objects.filter(Q(users=request.user) | Q(owner=request.user)).distinct()
        serializer = UsersGroupSerializer(groups, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UsersGroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def places_list(request):
    if request.method == 'GET':
        groups = UsersGroup.objects.filter(Q(users=request.user) | Q(owner=request.user)).distinct()
        photos_id = list(groups.values_list('photos', flat=True))
        owned_photos = Photo.objects.filter(pk__in=photos_id)
        owned_places = Place.objects.filter(Q(owner=request.user))
        owned_places = list(owned_places)
        places = [elem.place for elem in owned_photos]
        places.extend(owned_places)
        places = set(places)

        serializer = PlaceSerializer(places, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PlaceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def images_list(request):
    if request.method == 'GET':
        groups = UsersGroup.objects.filter(Q(users=request.user) | Q(owner=request.user)).distinct()
        photos_id = list(groups.values_list('photos', flat=True))
        owned_photos = Photo.objects.filter(pk__in=photos_id)
        owned_images = Image.objects.filter(Q(owner=request.user)).distinct()
        owned_images = list(owned_images)
        images = [elem.image for elem in owned_photos]
        images.extend(owned_images)
        images = set(images)
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def photos_list(request):
    if request.method == 'GET':
        groups = UsersGroup.objects.filter(Q(users=request.user) | Q(owner=request.user)).distinct()
        photos_id = list(groups.values_list('photos', flat=True))
        owned_photos = Photo.objects.filter(Q(pk__in=photos_id) | Q(owner=request.user))
        serializer = PhotoSerializer(owned_photos, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def group_detail(request, pk):
    try:
        group = UsersGroup.objects.filter(Q(users=request.user) | Q(owner=request.user)).distinct().get(pk=pk)
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


@api_view(['GET', 'PUT', 'DELETE'])
def place_detail(request, pk):
    try:
        groups = UsersGroup.objects.filter(Q(users=request.user) | Q(owner=request.user)).distinct()
        photos_id = list(groups.values_list('photos', flat=True))
        owned_photos = Photo.objects.filter(pk__in=photos_id)
        places = [elem.place for elem in owned_photos]
        place = Place.objects.get(pk=pk)
        if place not in places:
            raise Place.DoesNotExist
    except Place.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PlaceSerializer(place)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PlaceSerializer(place, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        place.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def image_detail(request, pk):
    try:
        groups = UsersGroup.objects.filter(Q(users=request.user) | Q(owner=request.user)).distinct()
        photos_id = list(groups.values_list('photos', flat=True))
        owned_photos = Photo.objects.filter(pk__in=photos_id)
        images = [elem.image for elem in owned_photos]
        image = Image.objects.get(pk=pk)
        if image not in images:
            raise Image.DoesNotExist
    except Image.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ImageSerializer(image)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ImageSerializer(image, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def photo_detail(request, pk):
    try:
        groups = UsersGroup.objects.filter(Q(users=request.user) | Q(owner=request.user)).distinct()
        photos_id = list(groups.values_list('photos', flat=True))
        owned_photos = list(Photo.objects.filter(pk__in=photos_id))
        photo = Photo.objects.get(pk=pk)
        if photo not in owned_photos:
            raise Photo.DoesNotExist
    except Photo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PhotoSerializer(photo)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PhotoSerializer(photo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        photo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LoginView(APIView):

    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = LoginSerializer(data=self.request.data,
                                     context={'request': self.request})

        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(None, status=status.HTTP_202_ACCEPTED)


class LogoutView(APIView):

    def get(self, request, format=None):
        logout(request)
        return Response(status=status.HTTP_200_OK)



