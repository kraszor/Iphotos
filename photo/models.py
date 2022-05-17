from django.db import models
from django.contrib.auth.models import User
from django.db.models import F
from django.urls import reverse
from .validators import validate_hashtags

# Create your models here.


class UsersGroup(models.Model):
    COLOR_CHOICES = [
        ('Green', 'Green'),
        ('Blue', 'Blue'),
        ('Red', 'Red'),
        ('Aqua', 'Aqua'),
        ('DarkBlue', 'DarkBlue'),
        ('Generic', 'Generic'),
        ('Orange', 'Orange'),
        ('Pink', 'Pink'),
        ('Violet', 'Violet'),
        ('Yellow', 'Yellow'),
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+', default=1, editable=False)
    name = models.fields.CharField(max_length=100)
    photo_count = models.fields.IntegerField(default=0, editable=False)
    tags = models.fields.CharField(max_length=200, default="#none", validators=[validate_hashtags])
    color_group = models.fields.CharField(max_length=10, choices=COLOR_CHOICES, default=None, null=True)
    is_local = models.fields.BooleanField(default=False, editable=False)
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
    album = models.ForeignKey(UsersGroup, on_delete=models.CASCADE, related_name='photos')
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.SET_DEFAULT, default='Unknown')

    def save(self, *args, **kwargs):
        super().save(self,*args, **kwargs)
        group = UsersGroup.objects.get(pk=self.album.id)
        group.photo_count += 1
        group.save()


