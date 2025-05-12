from rest_framework import viewsets, generics, permissions, filters, status
from rest_framework.decorators import action, api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from .models import User, Message, Notification, Service
from .serializers import (
    UserSerializer, MessageSerializer, NotificationSerializer, ServiceSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for user-related actions, such as registration, login, logout,
    filtering by user type, and profile updates.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['email', 'first_name', 'last_name']

    @action(detail=False, methods=['post'], url_path='register')
    def register(self, request):
        """
        Register a new user.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        """
        Log in a user and provide an auth token.
        """
        return ObtainAuthToken().post(request)

    @action(detail=False, methods=['post'], url_path='logout')
    def logout(self, request):
        """
        Log out a user by deleting their auth token.
        """
        if request.user.is_authenticated:
            request.user.auth_token.delete()
            return Response({"detail": "Logged out successfully."}, status=status.HTTP_200_OK)
        return Response({"detail": "User not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['get'], url_path='search-by-email')
    def search_by_email(self, request):
        """
        Search a user by email.
        """
        email = request.query_params.get('email')
        if not email:
            return Response({"detail": "Email parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(User, email=email)
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='clients')
    def get_clients(self, request):
        """
        Get all users with user_type='client'.
        """
        clients = User.objects.filter(user_type='client')
        serializer = self.get_serializer(clients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='service-providers')
    def get_service_providers(self, request):
        """
        Get all users with user_type='service_provider'.
        """
        service_providers = User.objects.filter(user_type='service_provider')
        serializer = self.get_serializer(service_providers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PasswordResetView(APIView):
    """
    A view to handle password reset requests.
    """
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"detail": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(email=email).first()
        if user:
            token = default_token_generator.make_token(user)
            reset_url = f"http://example.com/reset-password/{token}/"
            send_mail(
                "Password Reset",
                f"Click here to reset your password: {reset_url}",
                "noreply@example.com",
                [email]
            )
        return Response({"detail": "Password reset link sent if email exists."}, status=status.HTTP_200_OK)


class MessageViewSet(viewsets.ModelViewSet):
    """
    A viewset to handle messages between users.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Retrieve only messages related to the authenticated user.
        """
        return Message.objects.filter(receiver=self.request.user)

    def perform_create(self, serializer):
        """
        Automatically set the sender to the authenticated user.
        """
        serializer.save(sender=self.request.user)


class NotificationViewSet(viewsets.ModelViewSet):
    """
    A viewset to handle notifications for users.
    """
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Retrieve only notifications for the authenticated user.
        """
        return Notification.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'], url_path='mark-as-read')
    def mark_as_read(self, request, pk=None):
        """
        Mark a specific notification as read.
        """
        notification = self.get_object()
        notification.read = True
        notification.save()
        return Response({"detail": "Notification marked as read."}, status=status.HTTP_200_OK)


class ServiceSearchView(generics.ListAPIView):
    """
    API to search and filter services.
    """
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'location', 'category__name']
    ordering_fields = ['price', 'rating']