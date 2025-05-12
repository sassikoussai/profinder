from rest_framework import viewsets, permissions, filters
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.decorators import action

from .serializers import (UserSerializer, ServiceProviderProfileSerializer, ServiceCategorySerializer, ServiceSerializer, BookingSerializer)
from .models import (ServiceProviderProfile, Service_Category, Service, Booking, User)
from rest_framework.response import Response
from rest_framework import status

class UserViewSet (viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['get'])
    def get_user_by_email(self, request, email):
        user = get_object_or_404(User, email=email)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='clients')
    def get_clients(self, request):
        clients = User.objects.filter(user_type='client')
        serializer = UserSerializer(clients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def get_service_providers(self, request):
        service_providers = User.objects.filter(user_type='service_provider')
        serializer = UserSerializer(service_providers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)