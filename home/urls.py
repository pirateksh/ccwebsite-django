from django.urls import path
from home import views

urlpatterns = [
    path('', views.index, name="Index"),
    path('add-to-calendar/<int:pk>/',views.AddToCalendar,name="add-to-calendar"),
    # path('login/', views.login_view, name="Login"),
    path('login/', views.ajax_login_view, name="ajax_login"),
    # path('signup/', views.signup_view, name="Signup"),
    path('signup/', views.ajax_signup_view, name="ajax_signup"),
    path('logout/', views.logout_view, name="Logout"),
]
