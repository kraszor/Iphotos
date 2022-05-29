from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from .models import UsersGroup, Image, Place, Photo

# Create your tests here.


class UsersGroupModelTest(TestCase):
    def setUp(self):
        UsersGroup.objects.create(name='name',color_group='Aqua', description='xyz')
        User.objects.create(username='name', password='password')

    def test_fields_values(self):
        group = UsersGroup.objects.get(id=1)
        owner = group.owner
        name = group.name
        photo_count = group.photo_count
        tags = group.tags
        color = group.color_group
        is_local = group.is_local
        description = group.description
        self.assertEqual(name, 'name')
        self.assertEqual(owner.id, 1)
        self.assertEqual(photo_count, 0)
        self.assertEqual(tags, '#none')
        self.assertEqual(color, 'Aqua')
        self.assertEqual(is_local, False)
        self.assertEqual(description, 'xyz')

    def test_obj_update(self):
        group = UsersGroup.objects.get(id=1)
        group.name = 'new_name'
        group.save()
        self.assertEqual(group.name, 'new_name')


class ImageModelTest(TestCase):
    def setUp(self):
        Image.objects.create(source='abc', resolution_width=12, resolution_height=13, size=15)
        User.objects.create(username='name', password='password')

    def test_fields_values(self):
        image = Image.objects.get(id=1)
        source = image.source
        resolution_width = image.resolution_width
        resolution_height = image.resolution_height
        size = image.size
        self.assertEqual(source, 'abc')
        self.assertEqual(resolution_width, 12)
        self.assertEqual(resolution_height, 13)
        self.assertEqual(size, 15)

    def test_obj_update(self):
        image = Image.objects.get(id=1)
        image.source = 'new_source'
        image.save()
        self.assertEqual(image.source, 'new_source')


class PlaceModelTest(TestCase):
    def setUp(self):
        Place.objects.create(name='name', latitude=12, longitude=13)
        User.objects.create(username='name', password='password')

    def test_fields_values(self):
        place = Place.objects.get(id=1)
        name = place.name
        latitude = place.latitude
        longitude = place.longitude
        self.assertEqual(name, 'name')
        self.assertEqual(latitude, 12)
        self.assertEqual(longitude, 13)

    def test_obj_update(self):
        place = Place.objects.get(id=1)
        place.name = 'new_name'
        place.save()
        self.assertEqual(place.name, 'new_name')


class PhotoModelTest(TestCase):
    def setUp(self):
        date = datetime(2022, 5, 5, 0, 0, 0)
        User.objects.create(username='name', password='password')
        group = UsersGroup.objects.create(name='name', color_group='Aqua', description='xyz')
        image = Image.objects.create(source='abc', resolution_width=12, resolution_height=13, size=15)
        place = Place.objects.create(name='name', latitude=12, longitude=13)
        Photo.objects.create(title='title', tags='#none',
                             date_taken=date, album=group,
                             image=image, place=place)

    def test_fields_values(self):
        group = UsersGroup.objects.get(id=1)
        image = Image.objects.get(id=1)
        place = Place.objects.get(id=1)
        photo = Photo.objects.get(id=1)
        title = photo.title
        tags = photo.tags
        album = photo.album
        image_1 = photo.image
        place_1 = photo.place
        self.assertEqual(title, 'title')
        self.assertEqual(tags, '#none')
        self.assertEqual(album, group)
        self.assertEqual(image_1, image)
        self.assertEqual(place_1, place)
        self.assertEqual(group.photo_count, 1)

    def test_obj_update(self):
        photo = Photo.objects.get(id=1)
        photo.title = 'new_title'
        photo.save()
        self.assertEqual(photo.title, 'new_title')


class URLTests(TestCase):
    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_download_page(self):
        response = self.client.get('/download/')
        self.assertEqual(response.status_code, 200)

    def test_group_create(self):
        response = self.client.get('/group/create/')
        self.assertEqual(response.status_code, 302)

    def test_groups(self):
        response = self.client.get('/groups')
        self.assertEqual(response.status_code, 302)

    def test_api(self):
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, 200)

    def test_api_login(self):
        response = self.client.get('/api/login')
        self.assertEqual(response.status_code, 405)

    def test_api_logout(self):
        response = self.client.get('/api/logout')
        self.assertEqual(response.status_code, 403)

    def test_api_groups(self):
        response = self.client.get('/api/groups')
        self.assertEqual(response.status_code, 403)

    def test_api_places(self):
        response = self.client.get('/api/places')
        self.assertEqual(response.status_code, 403)

    def test_images(self):
        response = self.client.get('/api/images')
        self.assertEqual(response.status_code, 403)

    def test_api_photos(self):
        response = self.client.get('/api/photos')
        self.assertEqual(response.status_code, 403)

