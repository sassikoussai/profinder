from rest_framework.routers import DefaultRouter
from django.urls import path, include

from users.views import (
    UserViewSet)

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
app_name = 'users'
urlpatterns = [
    path('', include(router.urls)),
]