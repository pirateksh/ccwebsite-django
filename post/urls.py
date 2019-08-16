from django.urls import path
from . import views

urlpatterns = [
    # path('add/', views.add_post, name="Add Post"),
    path('ajax_add/', views.ajax_add_post, name="ajax_add_post"),
    path('delete/', views.ajax_del_post, name="ajax_delete_post"),
    path('edit/', views.ajax_edit_post, name="ajax_edit_post"),
    path('<slug:slug>/like/', views.post_like_toggle, name="like_toggle"),
    # path('api/<slug:slug>/like/', views.PostLikeAPIToggle.as_view(), name="like_api_toggle"),
]
