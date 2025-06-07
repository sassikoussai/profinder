from datetime import timezone
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import User, ServiceProviderProfile, Service_Category, Service, Booking


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'user_type', 'phone_number', 'address']
        read_only_fields = ['id']


class ServiceProviderProfileSerializer(ModelSerializer):

    class Meta:
        model = ServiceProviderProfile
        fields = ['user', 'profession', 'location', 'service_description', 'experience', 'rating']
        read_only_fields = ['rating']

    def validate_experience(self, value):
        if value < 0:
            raise serializers.ValidationError("Experience cannot be negative.")
        return value


class ServiceCategorySerializer(ModelSerializer):
    class Meta:
        model = Service_Category
        fields = ['id', 'name', 'description']
        read_only_fields = ['id']


class ServiceSerializer(ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'service_provider', 'category', 'title', 'description', 'price', 'location', 'is_active']
        read_only_fields = ['id']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value


# class BookingSerializer(ModelSerializer):
#     class Meta:
#         model = Booking
#         fields = ['id', 'service', 'client', 'booking_date', 'status','service_provider']
#         read_only_fields = ['id']

class BookingSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)
    service_provider = UserSerializer(read_only=True)
    client = UserSerializer(read_only=True)
    class Meta:
        model = Booking
        fields = ['id', 'service', 'client', 'booking_date', 'status', 'service_provider']
        read_only_fields = ['id']

   