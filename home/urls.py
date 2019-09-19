from django.urls import path
from home import views

urlpatterns = [

    # Active URL's - Intuitive name of paths
    path('', views.index, name="Index"),

    path('filter-post-by/<str:tag_filter>/', views.index, name="index_tag"),

    path('personalised/<str:username>/', views.index, name="personalised_index"),

    path('most-liked/<str:liked>/', views.index, name="index_most_liked"),

    path('older-first/<str:older>/', views.index, name="index_older_first"),

    path('most-liked/<str:liked>/personalised/<str:username>/', views.index, name="personalised_index_most_liked"),

    path('older-first/<str:older>/personalised/<str:username>/', views.index, name="personalised_index_older_first"),

    path(
        'filter-post-by/<str:tag_filter>/personalised/<str:username>/',
        views.index,
        name="personalised_index_with_filter"
    ),

    path('add-to-calendar/<int:pk>/', views.AddToCalendar, name="add-to-calendar"),
    # path('login/', views.login_view, name="Login"),

    path('login/', views.ajax_login_view, name="ajax_login"),
    path('signup/', views.ajax_signup_view, name="ajax_signup"),
    path('logout/', views.logout_view, name="Logout"),

    # Inactive URL's
    # path('login/', views.login_view, name="Login"),
    # path('signup/', views.signup_view, name="Signup"),
]
