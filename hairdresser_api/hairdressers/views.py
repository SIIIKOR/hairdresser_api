from django.contrib.auth.models import User

from rest_framework.viewsets import ModelViewSet

from hairdressers import serializers
from hairdressers import models

# Create your views here.
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class ServiceViewSet(ModelViewSet):
    queryset = models.Service.objects.all()
    serializer_class = serializers.ServiceSerializer


class HairdresserViewSet(ModelViewSet):
    queryset = models.Hairdresser.objects.all()
    serializer_class = serializers.HairdresserSerializer


class OrderViewSet(ModelViewSet):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer