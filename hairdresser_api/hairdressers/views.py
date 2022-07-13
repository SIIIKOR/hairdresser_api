from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db.models import ExpressionWrapper, F, DateTimeField
from django.utils import timezone

from rest_framework import viewsets, generics, authentication, permissions

from hairdressers import serializers
from hairdressers import models


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    queryset = models.Service.objects.all()
    serializer_class = serializers.ServiceSerializer

    def get_permissions(self):
        # Not logged in users can list and retrieve.
        if self.action in {'list', 'retrieve'}:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]


class HairdresserViewSet(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    queryset = models.Hairdresser.objects.all()
    serializer_class = serializers.HairdresserSerializer

    def get_permissions(self):
        # Not logged in users can list and retrieve.
        if self.action in {'list', 'retrieve'}:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]


class OrderViewSet(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]

    def get_permissions(self):
        # Only admin users can update, partial update and delete.
        if self.action in {'destroy', 'update', 'partial_update'}:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.request.user.is_staff: # type: ignore
            return models.Order.objects.all()
        elif self.request.user.is_authenticated:
            # Non admin users can do anything to their orders 
            # except update and partial update.
            return models.Order.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.user.is_staff: # type: ignore
            return serializers.OrderSerializer
        elif self.request.user.is_authenticated:
            # Non admin users user field is not mandatory,
            # but it must match request user.
            return serializers.UserOrderSerializer

    def perform_create(self, serializer):
        # If user is logged in but not admin,
        # fill user field with request user.
        if (self.request.user.is_authenticated and
                not self.request.user.is_staff): # type: ignore
            serializer.save(user=self.request.user)
        else: # Admin must provide user on post request.
            serializer.save()


class OccupiedOrderDateView(generics.ListAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.OccupiedOrderDateSerializer

    def get_queryset(self):
        return models.Order.objects.all().filter(
            hairdresser = get_object_or_404(
                models.Hairdresser, pk=self.kwargs.get("id")
            )
        ).annotate(
            end_time = ExpressionWrapper(
                F('start_time')+F('service__estimated_time'), 
                output_field=DateTimeField()
            )
        ).filter(
            start_time__gt=timezone.now()
        ).order_by('start_time')


class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    serializer_class = serializers.UserRegisterSerializer
