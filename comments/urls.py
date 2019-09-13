from django.urls import path
from . import views

urlpatterns = [
    # Active URL's - Intuitive name of path
    path('add/<int:post_id>/', views.ajax_add_comment, name='Add Comment'),

    # Inactive URL's
    # path('add/<int:post_id>/', views.add_comment, name='Add Comment'),
    # path('ajax_add/<int:post_id>/', views.ajax_add_comment, name="ajax_add_comment"),
]
