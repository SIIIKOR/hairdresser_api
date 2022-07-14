from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.db.models import ExpressionWrapper, F, DateTimeField, Q

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


class UserOrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Order
        fields = ['url', 'user', 'hairdresser', 'service', 'start_time']
        extra_kwargs = {
            'url': {'view_name': 'hairdressers:order-detail'},
            'user': {'view_name': 'hairdressers:user-detail', 'required':False},
            'hairdresser': {'view_name': 'hairdressers:hairdresser-detail'},
            'service': {'view_name': 'hairdressers:service-detail'}
        }

    def validate(self, data):
        # User who submitted post request.
        request_user = self.context.get('request').user # type:ignore
        # User submitted in post request. if none request user is used.
        submitted_user = data.get('user', request_user)
        if submitted_user != request_user:
            raise serializers.ValidationError("Provided user is not you.")
        
        start_time = data.get('start_time')
        end_time = start_time + data.get('service').estimated_time

        # Query to check if selected start_time and service by user creates
        # time frame which is not occupied by other user's order.
        overlapping_orders_count = models.Order.objects.filter(
            user=self.context.get('request').user, # type:ignore
            hairdresser=data.get('hairdresser')
        ).annotate(
            end_time = ExpressionWrapper(
                F('start_time')+F('service__estimated_time'), 
                output_field=DateTimeField()
            )
        ).filter(
            Q(start_time__range=(start_time, end_time)) |
            Q(end_time__range=(start_time, end_time))
        ).count()
        if overlapping_orders_count != 0:
            raise serializers.ValidationError(
                "This time is occupied by some other user."
            )
        return data


class OrderBookedDateViewSerializer(serializers.HyperlinkedModelSerializer):
    end_time = serializers.DateTimeField()

    class Meta:
        model = models.Order
        fields = ['url', 'start_time', 'end_time']
        extra_kwargs = {
            'url': {'view_name': 'hairdressers:order-detail'}
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
