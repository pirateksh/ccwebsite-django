from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views

urlpatterns = [
    path('admin/', admin.site.urls, name="Admin"),
    path('', include('home.urls')),
    path('post/', include('post.urls')),
    path('profile/', include('user_profile.urls')),

    # Account URLS

    url(r'^password_reset/$', views.PasswordResetView.as_view(), name='password_reset'),
    url(r'^password_reset/done/$', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'),
    url(r'^reset/done/$', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Extra URLS
    # url(r'^accounts/', include('allauth.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns += staticfiles_urlpatterns()
