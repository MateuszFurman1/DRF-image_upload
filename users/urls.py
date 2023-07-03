from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView, TokenBlacklistView,)
from users import views


urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/',views.RegisterView.as_view(), name='register'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('changepassword/', views.ChangePasswordView.as_view(), name='changepassword'),
    path('send-reset-password-email/', views.SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', views.PasswordResetView.as_view(), name='reset-password'),

]