from rest_framework.generics import ListAPIView
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from rest_framework import generics

class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_serializer_context(self):
        return {"request": self.request}


class ProductListView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.select_related("category").all()

        category_slug = self.request.query_params.get("category")
        featured = self.request.query_params.get("featured")
        search=self.request.query_params.get("search")      

        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        if featured == "true":
            queryset = queryset.filter(featured=True)
        if search:
            queryset=queryset.filter(name__icontains=search)

        return queryset.order_by("-created_at")

    def get_serializer_context(self):
        return {"request": self.request}
    

class ProductDetailBySlugView(generics.RetrieveAPIView):
    queryset = Product.objects.select_related("category").all()
    serializer_class = ProductSerializer
    lookup_field = "slug"