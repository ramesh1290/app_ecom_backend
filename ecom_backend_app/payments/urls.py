from django.urls import path
from .views import EsewaInitiatePaymentView, EsewaVerifyPaymentView

urlpatterns = [
    path("esewa/initiate/", EsewaInitiatePaymentView.as_view(), name="esewa-initiate"),
    path("esewa/verify/", EsewaVerifyPaymentView.as_view(), name="esewa-verify"),
]