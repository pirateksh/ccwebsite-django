from django.urls import path
from home import views

urlpatterns = [
    path('', views.index, name="Index"),
    path('login/', views.login_view, name="Login"),
    path('signup/', views.signup_view, name="Signup"),
    path('logout/', views.logout_view, name="Logout"),
]
