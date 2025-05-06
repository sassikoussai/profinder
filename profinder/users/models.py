from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('CLIENT', 'Client'),
        ('PROVIDER', 'Prestataire'),
        ('ADMIN', 'Administrateur'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='CLIENT')
    phone = models.CharField(max_length=8,validators=[
        RegexValidator(r'^\d{8}$', 'Le numéro de téléphone doit contenir 8 chiffres.')
    ], blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    postal_code = models.CharField(max_length=10, blank=True)
    