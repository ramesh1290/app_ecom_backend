from django.urls import path
from .views import ForgotPasswordAPIView, LoginView, RegisterView, ResetPasswordAPIView, VerifyOTPAPIView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
     path("login/", LoginView.as_view(), name="login"),
     path("forgot-password/", ForgotPasswordAPIView.as_view()),
    path("verify-otp/", VerifyOTPAPIView.as_view()),
    path("reset-password/", ResetPasswordAPIView.as_view()),
]