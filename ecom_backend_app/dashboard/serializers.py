from rest_framework import serializers
from contacts.models import Contact
from products.models import Product, Category
from payments.models import Order, OrderItem


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


class DashboardOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product_name",
            "product_price",
            "quantity",
            "total_price",
        ]


class DashboardOrderListSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()
    customer_email = serializers.SerializerMethodField()
    total_items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "customer_name",
            "customer_email",
            "transaction_uuid",
            "total_amount",
            "status",
            "esewa_ref_id",
            "created_at",
            "total_items",
        ]

    def get_customer_name(self, obj):
        if obj.user.first_name:
            return obj.user.first_name
        return obj.user.email

    def get_customer_email(self, obj):
        return obj.user.email

    def get_total_items(self, obj):
        return obj.items.count()


class DashboardOrderDetailSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()
    customer_email = serializers.SerializerMethodField()
    items = DashboardOrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "customer_name",
            "customer_email",
            "transaction_uuid",
            "total_amount",
            "tax_amount",
            "product_service_charge",
            "product_delivery_charge",
            "status",
            "esewa_ref_id",
            "esewa_transaction_code",
            "created_at",
            "items",
        ]

    def get_customer_name(self, obj):
        if obj.user.first_name:
            return obj.user.first_name
        return obj.user.email

    def get_customer_email(self, obj):
        return obj.user.email