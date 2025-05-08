from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import (User, ServiceProviderProfile, Service_Category, Service, Booking)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'user_type', 'phone_number', 'address']
        read_only_fields = ['id']
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

class ServiceProviderProfileSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = ServiceProviderProfile
        fields = ['user', 'profession', 'location', 'service_description', 'experience', 'rating']
        read_only_fields = ['user', 'rating']
        extra_kwargs = {
            'profession': {'required': True},
            'location': {'required': True},
            'service_description': {'required': True},
            'experience': {'required': True}
        }

class ServiceCategorySerializer(ModelSerializer):
    class Meta:
        model = Service_Category
        fields = ['id', 'name', 'description']
        read_only_fields = ['id']
        extra_kwargs = {
            'name': {'required': True},
            'description': {'required': True}
        }

class ServiceSerializer(ModelSerializer):
    service_provider = ServiceProviderProfileSerializer()

    class Meta:
        model = Service
        fields = ['id', 'service_provider', 'category', 'title', 'description', 'price', 'location', 'is_active']
        read_only_fields = ['id', 'service_provider']
        extra_kwargs = {
            'category': {'required': True},
            'title': {'required': True},
            'description': {'required': True},
            'price': {'required': True},
            'location': {'required': True}
        }

class BookingSerializer(ModelSerializer):
    service = ServiceSerializer()
    user = UserSerializer()

    class Meta:
        model = Booking
        fields = ['id', 'service', 'user', 'booking_date', 'status']
        read_only_fields = ['id', 'user']
        extra_kwargs = {
            'service': {'required': True},
            'booking_date': {'required': True},
            'status': {'required': True}
        }