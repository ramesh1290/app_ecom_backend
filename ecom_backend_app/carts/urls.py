from django.urls import path
from .views import (
    CartListView,
    AddToCartView,
    UpdateCartItemView,
    DeleteCartItemView,
)

urlpatterns = [
    path("cart/", CartListView.as_view(), name="cart-list"),
    path("cart/add/", AddToCartView.as_view(), name="cart-add"),
    path("cart/<int:pk>/update/", UpdateCartItemView.as_view(), name="cart-update"),
    path("cart/<int:pk>/delete/", DeleteCartItemView.as_view(), name="cart-delete"),
]