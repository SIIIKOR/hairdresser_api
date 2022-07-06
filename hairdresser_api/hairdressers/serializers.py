from django.contrib.auth.models import User
from rest_framework import serializers

from hairdressers.models import Service, Hairdresser, Order


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']
        extra_kwargs = {
            'url': {'view_name': 'hairdressers:user-detail'},
        }

class ServiceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Service
        fields = ['url', 'name', 'price', 'estimated_time']
        extra_kwargs = {
            'url': {'view_name': 'hairdressers:service-detail'},
        }


class HairdresserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Hairdresser
        fields = ['url', 'name', 'surname', 'email']
        extra_kwargs = {
            'url': {'view_name': 'hairdressers:hairdresser-detail'},
        }


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ['url', 'customer', 'hairdresser', 'service', 'start_time']
        extra_kwargs = {
            'url': {'view_name': 'hairdressers:order-detail'},
            'customer': {'view_name': 'hairdressers:user-detail'},
            'hairdresser': {'view_name': 'hairdressers:hairdresser-detail'},
            'service': {'view_name': 'hairdressers:service-detail'}
        }
