from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
import users.views

import blog.views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('blog.urls')),
    path('admin/', admin.site.urls, name='admin'),

    # Blog urls
    # Authentication Urls
    path('register/', users.views.register, name='register'),
    path('profile/', users.views.profile, name='profile'),

    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'), name='password_reset_complete'),

    path('password-change/', auth_views.PasswordChangeView.as_view(
        template_name='users/password_change.html'), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='users/password_change_done.html'), name='password_change_done'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
