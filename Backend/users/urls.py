from django.urls import path,include
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password-reset/',include('django_rest_passwordreset.urls'), name="password_reset"),
    path('password-reset/verify/', views.VerifyOTPAndResetPasswordView.as_view(), name='verify_otp_reset_password'),
]
