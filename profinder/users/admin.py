from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # Champs à afficher dans la liste des utilisateurs
    list_display = ('username', 'email', 'role', 'phone', 'city', 'is_staff')
    
    # Groupement des champs dans le formulaire d'édition
    fieldsets = UserAdmin.fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('role', 'phone', 'address', 'city', 'postal_code'),
        }),
    )
    
    # Champs disponibles lors de la création d'un utilisateur dans l'admin
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('role', 'phone', 'address', 'city', 'postal_code'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)