from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from hairdressers import serializers
from hairdressers import models

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    queryset = models.Service.objects.all()
    serializer_class = serializers.ServiceSerializer

    def get_permissions(self):
        # Non admin users can list and retrieve.
        if self.action in {'list', 'retrieve'}:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class HairdresserViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    queryset = models.Hairdresser.objects.all()
    serializer_class = serializers.HairdresserSerializer

    def get_permissions(self):
        # Non admin users can list and retrieve.
        if self.action in {'list', 'retrieve'}:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class OrderViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    serializer_class = serializers.OrderSerializer

    def get_permissions(self):
        # Only admin users and update and partial update.
        if self.action in {'update', 'partial_update'}:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.request.user.is_staff: # type: ignore
            return models.Order.objects.all()
        elif self.request.user.is_authenticated:
            # Non admin users can do anything to their orders except update and partial update.
            return models.Order.objects.filter(user=self.request.user)


class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = serializers.UserRegisterSerializer
