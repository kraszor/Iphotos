from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class UsersGroup(models.Model):
    # owner = models.CharField(max_length=100, default=None, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+', default=None, editable=True)
    name = models.fields.CharField(max_length=150)
    photo_count = models.fields.IntegerField(default=0)
    tags = models.fields.CharField(max_length=200, default="empty")
    color_group = models.fields.CharField(max_length=50, default="unknown")
    is_local = models.fields.BooleanField(default=False)
    create_time = models.fields.DateTimeField(auto_now_add=True)
    edit_time = models.fields.DateTimeField(auto_now=True)
    description = models.fields.TextField(max_length=500)
    users = models.ManyToManyField(User, blank=True)
    # .objects.exclude(owner)

    def get_absolute_url(self):
        return reverse('photo:home')


class Image(models.Model):
    source = models.CharField(max_length=150)
    resolution_width = models.fields.IntegerField()
    resolution_height = models.fields.IntegerField()
    size = models.fields.DecimalField(max_digits=5, decimal_places=3)


class Place(models.Model):
    name = models.fields.CharField(max_length=100, default="Unknown")
    latitude = models.fields.DecimalField(null=True, blank=True, max_digits=4, decimal_places=2)
    longitude = models.fields.DecimalField(null=True, blank=True, max_digits=4, decimal_places=2)


class Photo(models.Model):
    title = models.fields.CharField(max_length=150)
    tags = models.fields.CharField(max_length=300)
    date_taken = models.fields.DateTimeField()
    album = models.ForeignKey(UsersGroup, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.SET_DEFAULT, default='Unknown')


