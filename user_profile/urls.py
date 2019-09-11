# from django.contrib import admin
from django.urls import path
# from django.conf.urls import url
from . import views

urlpatterns = [
    path('<str:username>/', views.user_profile, name="User Profile"),
    path('<str:username>/avatar_upload/', views.avatar_upload, name="Avatar Upload"),
    path('<str:username>/change_password/', views.change_password, name="Change Password"),
    path('<str:username>/drafts/', views.show_drafts, name="Drafts"),
    path('<str:username>/edit_profile/', views.edit_profile, name="edit_profile"),
    path('<str:username>/filter_by_post/<str:tag_name>', views.user_profile, name='filter_post_user_profile'),
]
