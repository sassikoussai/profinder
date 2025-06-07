from rest_framework import viewsets, generics, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from .models import Booking, Service_Category, ServiceProviderProfile, User, Service
from .serializers import (
    BookingSerializer, ServiceProviderProfileSerializer, UserSerializer, ServiceSerializer,ServiceCategorySerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for user-related actions, including registration, login, logout,
    filtering by user type, and profile management.
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
        Log in a user and return an authentication token.
        """
        class CustomObtainAuthToken(ObtainAuthToken):
            def post(self, request, *args, **kwargs):
                response = super().post(request, *args, **kwargs)
                token = Token.objects.get(key=response.data['token'])
                user = User.objects.get(id=token.user_id)
                return Response({
                    'token': token.key,
                    'user': {
                        'id': user.id,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                    }
                })

        custom_auth_view = CustomObtainAuthToken.as_view()
        return custom_auth_view(request)

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



class ServiceSearchView(generics.ListAPIView):
    """
    API to search and filter services.
    """
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'location', 'category__name']
    ordering_fields = ['price', 'rating']


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all().order_by('-booking_date')
    serializer_class = BookingSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        client_id = self.request.query_params.get('client')
        provider_id = self.request.query_params.get('service_provider')
        
        if client_id:
            queryset = queryset.filter(client__id=client_id)
        if provider_id:
            queryset = queryset.filter(service_provider__id=provider_id)
        return queryset

class ServiceCategoryViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing service categories.
    """
    queryset = Service_Category.objects.all()
    serializer_class = ServiceCategorySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset
    
class ServiceViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing services.
    """
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category__id=category_id)
        return queryset

class ServiceProviderProfileViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing service provider profiles.
    """
    queryset = ServiceProviderProfile.objects.all()
    serializer_class = ServiceProviderProfileSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        profession = self.request.query_params.get('profession')
        if profession:
            queryset = queryset.filter(profession__icontains=profession)
        return queryset