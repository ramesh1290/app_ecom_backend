from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "image",
            "product_count",
            "description",
        ]

    def get_image(self, obj):
        
        if obj.image:
            return obj.image.url
        return None

    def get_product_count(self, obj):
        return obj.products.count()


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    category_name = serializers.CharField(source="category.name", read_only=True)
    category_slug = serializers.CharField(source="category.slug", read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "price",
            "image",
            "featured",
            "stock",
            "category",
            "category_name",
            "category_slug",
        ]

    def get_image(self, obj):
        
        if obj.image:
            return obj.image.url
        return None