from django.urls import path
from .views import (
    PasswordResetRequestView,
    PasswordResetConfirmView,
    register,
    ProfileDetailView
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import ProfileDetailView
urlpatterns = [
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    
    path('register/',register),
    #path('profile/', profile),
     path('profile/', ProfileDetailView.as_view(), name='profile'),

    
    path("password-reset/", PasswordResetRequestView.as_view()),
    path("password-reset-confirm/<uid>/<token>/", PasswordResetConfirmView.as_view()),
]
