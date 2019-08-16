from django.urls import path
from . import views

urlpatterns = [
    # path('add/<int:post_id>/', views.add_comment, name='Add Comment'),
    path('add/<int:post_id>/', views.ajax_add_comment, name='Add Comment'),
    # path('ajax_add/<int:post_id>/', views.ajax_add_comment, name="ajax_add_comment"),
]
