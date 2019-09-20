# from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    # Active URL's - Intuitive paths.
    path('<str:username>/', views.user_profile, name="User Profile"),
    path('<str:username>/avatar_upload/', views.avatar_upload, name="Avatar Upload"),
    path('<str:username>/change_password/', views.change_password, name="Change Password"),
    path('<str:username>/drafts/', views.show_drafts, name="Drafts"),
    path('<str:username>/edit_profile/', views.edit_profile, name="edit_profile"),
    path('<str:username>/filter_by_post/<str:tag_name>/', views.user_profile, name='filter_post_user_profile'),
    path('<str:username>/most-liked/', views.user_profile, name='most_liked_user_profile'),
    path('<str:username>/older-first/', views.user_profile, name='older_first_user_profile'),
    path('<str:username>/change_name/', views.change_name, name='change_name'),
    path('<str:username>/change_email/', views.change_email, name='change_email'),
    path('<str:username>/subscription_toggle/', views.subscription_toggle, name='subscription_toggle'),
    path('<str:username>/sound_toggle/', views.sound_notification_toggle, name='sound_notification_toggle'),
    path('<str:username>/set_password/', views.set_password, name='set_password'),
    path('<str:username>/approve_event/<slug:slug>', views.approve_event, name='approve_event'),
    path('<str:username>/reject_event/<slug:slug>', views.reject_event, name='reject_event'),
    path('<str:username>/get_calendar/',views.get_user_calendar,name="get_user_calendar"),
    path('<str:username>/verify_email/', views.verify_email, name='verify_email'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path('<str:username>/follow_user/<str:username2>/', views.follow_user, name='follow_user'),
    path('<str:username>/unfollow_user/<str:username2>/', views.unfollow_user, name='unfollow_user'),
    path('<str:username>/subscribe_to/<str:tag>', views.subscribe_to_tag_toggle, name='subscribe_to_tag_toggle'),
]
