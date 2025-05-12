from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import User, ServiceProviderProfile, ServiceCategory, Service, Booking


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'user_type', 'phone_number', 'address']
        read_only_fields = ['id']

    def validate_email(self, value):
        if not value.endswith('@example.com'):
            raise serializers.ValidationError("Only example.com emails are allowed.")
        return value


class ServiceProviderProfileSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = ServiceProviderProfile
        fields = ['user', 'profession', 'location', 'service_description', 'experience', 'rating']
        read_only_fields = ['user', 'rating']

    def validate_experience(self, value):
        if value < 0:
            raise serializers.ValidationError("Experience cannot be negative.")
        return value


class ServiceCategorySerializer(ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ['id', 'name', 'description']
        read_only_fields = ['id']


class ServiceSerializer(ModelSerializer):
    service_provider = ServiceProviderProfileSerializer(read_only=True)

    class Meta:
        model = Service
        fields = ['id', 'service_provider', 'category', 'title', 'description', 'price', 'location', 'is_active']
        read_only_fields = ['id', 'service_provider']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value


class BookingSerializer(ModelSerializer):
    service = ServiceSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'service', 'client', 'booking_date', 'status']
        read_only_fields = ['id', 'service']

    def validate_booking_date(self, value):
        from datetime import datetime
        if value < datetime.now():
            raise serializers.ValidationError("Booking date cannot be in the past.")
        return value