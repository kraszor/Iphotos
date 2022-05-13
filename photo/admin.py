from django.contrib import admin
from .models import UsersGroup, Place, Image, Photo

# Register your models here.
admin.site.register(UsersGroup)
admin.site.register(Place)
admin.site.register(Image)
admin.site.register(Photo)