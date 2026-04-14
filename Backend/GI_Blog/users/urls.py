from django.urls import path
from .views import PasswordResetRequestView, PasswordResetConfirmView, register, profile
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    
    path('register/',register),
    path('profile/', profile),

    
    path("password-reset/", PasswordResetRequestView.as_view()),
    path("password-reset-confirm/<uid>/<token>/", PasswordResetConfirmView.as_view()),
]
