from django.contrib.auth.models import User
from rest_framework import serializers


from hairdressers.models import Service, Hairdresser, Order


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class ServiceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Service
        fields = ['url', 'name', 'price', 'estimated_time']


class HairdresserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Hairdresser
        fields = ['url', 'name', 'surname', 'email']


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ['url', 'customer', 'hairdresser', 'service', 'start_time']