from django.contrib.auth.models import User

from rest_framework import serializers

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
        fields = ['url', 'customer', 'hairdresser', 'service', 'start_time']
        extra_kwargs = {
            'url': {'view_name': 'hairdressers:order-detail'},
            'customer': {'view_name': 'hairdressers:user-detail'},
            'hairdresser': {'view_name': 'hairdressers:hairdresser-detail'},
            'service': {'view_name': 'hairdressers:service-detail'}
        }
