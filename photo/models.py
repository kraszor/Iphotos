from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class UsersGroup(models.Model):
    name = models.fields.CharField(max_length=150)
    create_time = models.fields.DateTimeField(auto_now_add=True)
    edit_time = models.fields.DateTimeField(auto_now=True)
    description = models.fields.TextField(max_length=500)
    users = models.ManyToManyField(User)

    def get_absolute_url(self):
        return reverse('photo:home')
