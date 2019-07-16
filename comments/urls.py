from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:post_id>/', views.add_comment, name='Add Comment'),
]
