from rest_framework import serializers
from users.models import (
    User, ServiceProviderProfile, ServiceCategory, Service,
    Booking, Message, Notification
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'user_type', 'phone_number', 'address']
        read_only_fields = ['id']


class ServiceProviderProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = ServiceProviderProfile
        fields = ['user', 'profession', 'location', 'service_description', 'experience', 'rating']


class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ['id', 'name', 'description']


class ServiceSerializer(serializers.ModelSerializer):
    service_provider = ServiceProviderProfileSerializer(read_only=True)

    class Meta:
        model = Service
        fields = ['id', 'service_provider', 'category', 'title', 'description', 'price', 'location', 'is_active']


class BookingSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'service', 'client', 'service_provider', 'booking_date', 'status']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'created_at']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'read', 'created_at']