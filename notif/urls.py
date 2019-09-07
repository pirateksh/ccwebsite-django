from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.notification_view, name="all_notifications"),
    path('mark_as_read/<int:pk>', views.mark_as_read, name="mark_as_read"),
    path('mark_all_as_read/', views.mark_all_as_read, name="mark_all_as_read"),
    path('clear/<int:pk>', views.clear_notification, name="clear_notification"),
    path('clear_all/', views.clear_all_notification, name="clear_all_notification"),
]
