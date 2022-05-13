from rest_framework import serializers
from .models import UsersGroup, Place, Photo, Image


class UsersGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersGroup
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'
