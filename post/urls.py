from django.urls import path
from post import views

urlpatterns = [
    path('add/', views.add_post, name="Add Post"),
]
