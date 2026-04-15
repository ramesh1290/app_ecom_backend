from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import CartItem
from .serializers import CartItemSerializer
from products.models import Product


class CartListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart_items = CartItem.objects.filter(user=request.user).select_related("product")
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product")
        try:
            quantity = int(request.data.get("quantity", 1))
        except (TypeError, ValueError):
            return Response(
                {"message": "Quantity must be a valid number."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if quantity < 1:
            return Response(
        {"message": "Quantity must be at least 1."},
        status=status.HTTP_400_BAD_REQUEST,
           )

        if not product_id:
            return Response(
                {"message": "Product id is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        product = get_object_or_404(Product, id=product_id)

        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={"quantity": quantity},
        )

        if not created:
            cart_item.quantity = quantity
            cart_item.save()

        serializer = CartItemSerializer(cart_item)
        return Response(
            {
                "message": "Product added to cart successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


class UpdateCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        cart_item = get_object_or_404(
            CartItem.objects.select_related("product"),
            pk=pk,
            user=request.user
        )

        quantity = request.data.get("quantity")

        if quantity is None:
            return Response(
                {"message": "Quantity is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        quantity = int(quantity)

        if quantity < 1:
            cart_item.delete()
            return Response(
                {"message": "Cart item removed."},
                status=status.HTTP_200_OK,
            )

        cart_item.quantity = quantity
        cart_item.save()

        serializer = CartItemSerializer(cart_item)
        return Response(
            {
                "message": "Cart updated successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class DeleteCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        cart_item = get_object_or_404(CartItem, pk=pk, user=request.user)
        cart_item.delete()

        return Response(
            {"message": "Cart item deleted successfully."},
            status=status.HTTP_200_OK,
        )