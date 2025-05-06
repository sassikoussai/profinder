from django.shortcuts import render
from .models import CustomUser
from django.http import JsonResponse

def register_provider(request):
    if request.method == 'POST':
        # Exemple de création d'un prestataire
        user = CustomUser.objects.create_user(
            username=request.POST.get('username'),
            password=request.POST.get('password'),
            role='PROVIDER',
            phone=request.POST.get('phone'),
            city=request.POST.get('city')
        )
        return JsonResponse({'status': 'success', 'user_id': user.id})
    return JsonResponse({'status': 'error'}, status=400)