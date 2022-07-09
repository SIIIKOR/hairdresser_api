from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from hairdressers import models


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']
        extra_kwargs = {
            'url': {'view_name': 'hairdressers:user-detail'},
        }

class ServiceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Service
        fields = ['url', 'name', 'price', 'estimated_time']
        extra_kwargs = {
            'url': {'view_name': 'hairdressers:service-detail'},
        }


class HairdresserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Hairdresser
        fields = ['url', 'name', 'surname', 'email']
        extra_kwargs = {
            'url': {'view_name': 'hairdressers:hairdresser-detail'},
        }


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Order
        fields = ['url', 'user', 'hairdresser', 'service', 'start_time']
        extra_kwargs = {
            'url': {'view_name': 'hairdressers:order-detail'},
            'user': {'view_name': 'hairdressers:user-detail'},
            'hairdresser': {'view_name': 'hairdressers:hairdresser-detail'},
            'service': {'view_name': 'hairdressers:service-detail'}
        }


class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "password2"]

    def validate(self, data):
        if data.get("password") != data.get("password2"):
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return data

    def create(self, validated_data):
        user = User.objects.create_user( # type: ignore
            username=validated_data.get("username"),
            email=validated_data.get("email"),
            password=validated_data.get("password")
        )
        return user
