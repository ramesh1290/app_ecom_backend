from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "category", "price", "featured", "stock"]
    list_filter = ["category", "featured"]
    search_fields = ["name", "category__name"]
    prepopulated_fields = {"slug": ("name",)}