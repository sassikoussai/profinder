from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(models.Model):
    USER_TYPE_CHOICES = (
        ('client', 'Client'),
        ('service_provider', 'Service Provider'),
    )

    # Base fields
    email = models.EmailField(_('email address'), unique=True)
    phone_regex = RegexValidator(
        regex=r'^\+?[0-9]{8,15}$',
        message="Enter a valid phone number."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='client')
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

    @property
    def is_client(self):
        return self.user_type == 'client'

    @property
    def is_service_provider(self):
        return self.user_type == 'service_provider'





class ServiceProviderProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'service_provider'}
    )
    profession = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True)
    service_description = models.TextField(blank=True)
    experience = models.IntegerField(default=0)
    rating = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Service Provider Profile for {self.user.email}"


class Service(models.Model):
    service_provider = models.ForeignKey(
        ServiceProviderProfile,
        on_delete=models.CASCADE,
        related_name='services'
    )
    category = models.ForeignKey('Service_Category', on_delete=models.CASCADE, related_name='services',default=0)
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.service_provider.user.email}"

class Service_Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'category'

    def __str__(self):
        return self.name

class Booking (models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    client = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'client'})
    service_provider = models.ForeignKey(ServiceProviderProfile, on_delete=models.CASCADE, limit_choices_to={'user_type': 'service_provider'})
    booking_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('completed', 'Completed')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Booking for {self.service.title} by {self.client.email}"