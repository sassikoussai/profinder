from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(models.Model):
    USER_TYPE_CHOICES = (
        ('client', 'Client'),
        ('service_provider', 'Service Provider'),
    )

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


class ServiceCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    service_provider = models.ForeignKey(
        ServiceProviderProfile,
        on_delete=models.CASCADE,
        related_name='services'
    )
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='services')
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.service_provider.user.email}"


class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
    )

    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'client'}
    )
    service_provider = models.ForeignKey(
        ServiceProviderProfile,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'service_provider'}
    )
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    booking_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Booking by {self.client.email} for {self.service.title}"


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.email} to {self.receiver.email}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.email}"