from rest_framework.routers import DefaultRouter
from django.urls import path, include

from users.views import (
    BookingViewSet,
    ServiceCategoryViewSet,
    ServiceProviderProfileViewSet,
    ServiceViewSet,
    UserViewSet)

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'service-categories', ServiceCategoryViewSet, basename='service-category')
router.register(r'services', ServiceViewSet, basename='service')
router.register(r'service-providers-profile', ServiceProviderProfileViewSet, basename='service-provider-profile')
app_name = 'users'
urlpatterns = [
    path('', include(router.urls)),
]