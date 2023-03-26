from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework.authtoken.admin import User
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Profile

class SignupView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        if not username or not password:
            return JsonResponse({'error': 'Username and password are required'}, status=400)
        user = User.objects.create_user(username=username, password=password)
        Profile.objects.create(user=user, first_name=first_name, last_name=last_name)
        return JsonResponse({'message': 'User created successfully'}, status=201)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if not user:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
        login(request, user)
        refresh = RefreshToken.for_user(user)
        return JsonResponse({'access_token': str(refresh.access_token)}, status=200)

class ProfileView(APIView):
    @login_required
    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        return JsonResponse({'first_name': profile.first_name, 'last_name': profile.last_name}, status=200)

    @login_required
    def put(self, request):
        profile = Profile.objects.get(user=request.user)
        first_name = request.data.get('first_name', profile.first_name)
        last_name = request.data.get('last_name', profile.last_name)
        profile.first_name = first_name
        profile.last_name = last_name
        profile.save()
        return JsonResponse({'message': 'Profile updated successfully'}, status=200)

class DeleteView(APIView):
    @login_required
    def delete(self, request):
        request.user.delete()
        logout(request)
        return JsonResponse({'message': 'Profile deleted successfully'}, status=200)