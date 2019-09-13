from django.urls import path
from home import views

urlpatterns = [

    # Active URL's - Intuitive name of paths
    path('', views.index, name="Index"),
    path('filter-post-by/<str:tag_filter>/', views.index, name="index_tag"),
    path('login/', views.ajax_login_view, name="ajax_login"),
    path('signup/', views.ajax_signup_view, name="ajax_signup"),
    path('logout/', views.logout_view, name="Logout"),

    # Inactive URL's
    # path('login/', views.login_view, name="Login"),
    # path('signup/', views.signup_view, name="Signup"),
]
