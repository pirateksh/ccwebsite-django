from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views
import notifications.urls

urlpatterns = [
    path('admin/', admin.site.urls, name="Admin"),
    path('', include('home.urls')),
    path('',include('quizapp.urls')),
    path('post/', include('post.urls')),
    path('profile/', include('user_profile.urls')),
    path('comments/', include('comments.urls')),
    path('notification/', include('notif.urls')),

    # Account URLS
    url(r'^password_reset/$', views.PasswordResetView.as_view(), name='password_reset'),
    url(r'^password_reset/done/$', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'),
    url(r'^reset/done/$', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Extra URLS
    path('ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),



    # url(r'^accounts/', includes('allauth.urls')),
    # oauth/ url will be accessed by Social site link to take to their website.


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns += staticfiles_urlpatterns()
