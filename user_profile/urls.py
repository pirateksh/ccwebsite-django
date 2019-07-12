from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('<str:username>/', views.user_profile, name="User Profile"),
    path('avatar_upload/<str:username>/', views.avatar_upload, name="Avatar Upload"),
    path('change_password/<str:username>', views.change_password, name="Change Password"),
]
