from django.contrib.auth.models import User

from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from hairdressers import serializers
from hairdressers import models

# Create your views here.
class UserViewSet(ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class ServiceViewSet(ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = models.Service.objects.all()
    serializer_class = serializers.ServiceSerializer


class HairdresserViewSet(ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = models.Hairdresser.objects.all()
    serializer_class = serializers.HairdresserSerializer


class OrderViewSet(ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer