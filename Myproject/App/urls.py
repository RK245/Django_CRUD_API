from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('signup',views.SignupView.as_view()),
    path('login',views.LoginView.as_view()),
    path('profile',views.ProfileView.as_view()),
    path('delete',views.DeleteView.as_view()),
]
