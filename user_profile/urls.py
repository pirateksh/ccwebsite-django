# from django.contrib import admin
from django.urls import path
# from django.conf.urls import url
from . import views

urlpatterns = [
    # Active URL's - Intuitive paths.
    path('<str:username>/', views.user_profile, name="User Profile"),
    path('<str:username>/avatar_upload/', views.avatar_upload, name="Avatar Upload"),
    path('<str:username>/change_password/', views.change_password, name="Change Password"),
    path('<str:username>/drafts/', views.show_drafts, name="Drafts"),
    path('<str:username>/edit_profile/', views.edit_profile, name="edit_profile"),
    path('<str:username>/filter_by_post/<str:tag_name>/', views.user_profile, name='filter_post_user_profile'),
    path('<str:username>/change_name/', views.change_name, name='change_name'),
    path('<str:username>/change_email/', views.change_email, name='change_email'),
    path('<str:username>/subscription_toggle/', views.subscription_toggle, name='subscription_toggle'),
    # path('<str:username>/subscribe/', views.subscribe, name='subscribe'),
    path('<str:username>/sound_toggle/', views.sound_notification_toggle, name='sound_notification_toggle'),
    path('<str:username>/set_password/', views.set_password, name='set_password'),
    path('<str:username>/ask_perm/', views.ask_perm, name='ask_perm'),
]
