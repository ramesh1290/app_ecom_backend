from rest_framework import serializers
from contacts.models import Contact
from products.models import Product,Category


class DashboardProductSerializer(serializers.ModelSerializer):
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
        read_only_fields = ["slug"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")

        if instance.image and request:
            data["image"] = request.build_absolute_uri(instance.image.url)
        else:
            data["image"] = None

        return data
    
class DashboardCategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "image",
            "product_count",
        ]
        read_only_fields = ["slug"]

    def get_product_count(self, obj):
        return obj.products.count()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")

        if instance.image and request:
            data["image"] = request.build_absolute_uri(instance.image.url)
        else:
            data["image"] = None

        return data
    
class DashboardContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"