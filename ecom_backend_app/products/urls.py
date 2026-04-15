# products/urls.py

from django.urls import path
from .views import CategoryListView, ProductDetailBySlugView, ProductListView

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path("products/", ProductListView.as_view(), name="product-list"),
    path("products/<slug:slug>/", ProductDetailBySlugView.as_view(), name="product-detail"),
]