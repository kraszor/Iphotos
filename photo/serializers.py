from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import UsersGroup, Place, Photo, Image
from django.contrib.auth.models import User


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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'date_joined']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(label="Username", write_only=True)
    password = serializers.CharField(label="Password",
                                     style={'input_type': 'password'},
                                     trim_whitespace=False,
                                     write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(requests=self.context.get('request'),
                                username=username, password=password)
            if not user:
                msg = 'Wrong username or password! Access denied!'
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = 'You have to enter both username and password'
            raise serializers.ValidationError(msg, code="authorization")
        attrs['user'] = user
        return attrs

