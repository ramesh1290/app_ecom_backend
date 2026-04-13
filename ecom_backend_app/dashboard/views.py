from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from products.models import Product, Category
from contacts.models import Contact
from rest_framework import generics
from .serializers import DashboardCategorySerializer, DashboardContactSerializer, DashboardProductSerializer
from rest_framework.parsers import MultiPartParser, FormParser

class DashboardSummaryView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        total_products = Product.objects.count()
        total_categories = Category.objects.count()
        total_contacts = Contact.objects.count()
        featured_products = Product.objects.filter(featured=True).count()
        low_stock_products = Product.objects.filter(stock__lt=5).count()

        latest_products = Product.objects.select_related("category").order_by("-created_at")
        latest_contacts = Contact.objects.order_by("-id")

        products_data = [
            {
                "id": product.id,
                "name": product.name,
                "price": str(product.price),
                "stock": product.stock,
                "featured": product.featured,
                "category_name": product.category.name,
            }
            for product in latest_products
        ]

        contacts_data = [
            {
                "id": contact.id,
                "first_name": contact.first_name,
                "last_name": contact.last_name,
                "email": contact.email,
                "subject": contact.subject,
                "message": contact.message,
            }
            for contact in latest_contacts
        ]

        return Response({
            "total_products": total_products,
            "total_categories": total_categories,
            "total_contacts": total_contacts,
            "featured_products": featured_products,
            "low_stock_products": low_stock_products,
            "latest_products": products_data,
            "latest_contacts": contacts_data,
        })

class DashboardProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.select_related("category").order_by("-created_at")
    serializer_class = DashboardProductSerializer
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_context(self):
        return {"request": self.request}


class DashboardProductRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.select_related("category").all()
    serializer_class = DashboardProductSerializer
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_context(self):
        return {"request": self.request}
    
class DashboardCategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.order_by("-id")
    serializer_class = DashboardCategorySerializer
    permission_classes = [IsAdminUser]

    def get_serializer_context(self):
        return {"request": self.request}


class DashboardCategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = DashboardCategorySerializer
    permission_classes = [IsAdminUser]

    def get_serializer_context(self):
        return {"request": self.request}
    
class DashboardContactListView(generics.ListAPIView):
    queryset = Contact.objects.all().order_by("-id")
    serializer_class = DashboardContactSerializer
    permission_classes = [IsAdminUser]


class DashboardContactDeleteView(generics.DestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = DashboardContactSerializer
    permission_classes = [IsAdminUser]