import uuid
import requests
from decimal import Decimal

from django.conf import settings
from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from carts.models import CartItem
from .models import Order, OrderItem
from .serializers import EsewaInitSerializer
from .utils import (
    generate_esewa_signature,
    verify_esewa_response_signature,
    decode_base64_response,
)


class EsewaInitiatePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        serializer = EsewaInitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart_items = CartItem.objects.filter(user=request.user).select_related("product")

        if not cart_items.exists():
            return Response(
                {"message": "Your cart is empty."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        subtotal = Decimal("0.00")
        for item in cart_items:
            subtotal += Decimal(str(item.product.price)) * item.quantity

        tax_amount = Decimal("0.00")
        product_service_charge = Decimal("0.00")
        product_delivery_charge = Decimal("0.00")
        total_amount = subtotal + tax_amount + product_service_charge + product_delivery_charge

        transaction_uuid = str(uuid.uuid4())

        order = Order.objects.create(
            user=request.user,
            transaction_uuid=transaction_uuid,
            total_amount=total_amount,
            tax_amount=tax_amount,
            product_service_charge=product_service_charge,
            product_delivery_charge=product_delivery_charge,
            status="PENDING",
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.name,
                product_price=item.product.price,
                quantity=item.quantity,
                total_price=Decimal(str(item.product.price)) * item.quantity,
            )

        total_amount_str = f"{total_amount:.2f}"
        signature = generate_esewa_signature(
            secret_key=settings.ESEWA_SECRET_KEY,
            total_amount=total_amount_str,
            transaction_uuid=transaction_uuid,
            product_code=settings.ESEWA_PRODUCT_CODE,
        )

        success_url = f"{settings.FRONTEND_BASE_URL}/payment/esewa/success"
        failure_url = f"{settings.FRONTEND_BASE_URL}/payment/esewa/failure"

        payload = {
            "amount": f"{subtotal:.2f}",
            "tax_amount": f"{tax_amount:.2f}",
            "total_amount": total_amount_str,
            "transaction_uuid": transaction_uuid,
            "product_code": settings.ESEWA_PRODUCT_CODE,
            "product_service_charge": f"{product_service_charge:.2f}",
            "product_delivery_charge": f"{product_delivery_charge:.2f}",
            "success_url": success_url,
            "failure_url": failure_url,
            "signed_field_names": "total_amount,transaction_uuid,product_code",
            "signature": signature,
        }

        return Response(
            {
                "message": "eSewa payment initiated.",
                "form_url": settings.ESEWA_FORM_URL,
                "payload": payload,
            },
            status=status.HTTP_200_OK,
        )


class EsewaVerifyPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        encoded_data = request.data.get("data")

        if not encoded_data:
            return Response(
                {"message": "Missing eSewa response data."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            decoded_data = decode_base64_response(encoded_data)
        except Exception:
            return Response(
                {"message": "Invalid eSewa response format."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not verify_esewa_response_signature(settings.ESEWA_SECRET_KEY, decoded_data):
            return Response(
                {"message": "Invalid eSewa response signature."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        transaction_uuid = decoded_data.get("transaction_uuid")
        total_amount = decoded_data.get("total_amount")
        status_value = decoded_data.get("status")
        transaction_code = decoded_data.get("transaction_code")

        if not transaction_uuid or status_value != "COMPLETE":
            return Response(
                {"message": "Payment not completed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        order = get_object_or_404(
            Order,
            transaction_uuid=transaction_uuid,
            user=request.user,
        )

        status_check_params = {
            "product_code": settings.ESEWA_PRODUCT_CODE,
            "total_amount": total_amount,
            "transaction_uuid": transaction_uuid,
        }

        try:
            esewa_status_response = requests.get(
                settings.ESEWA_STATUS_CHECK_URL,
                params=status_check_params,
                timeout=15,
            )
            esewa_status_response.raise_for_status()
            status_json = esewa_status_response.json()
        except Exception as e:
            return Response(
                {"message": "Failed to verify payment with eSewa status API.",
                  "error": str(e),
                  "url": settings.ESEWA_STATUS_CHECK_URL,
                  "params": status_check_params,
                    "raw_response": getattr(esewa_status_response, "text", None) if "esewa_status_response" in locals() else None,
                 
                 },
                
                

                status=status.HTTP_502_BAD_GATEWAY,
            )

        if status_json.get("status") != "COMPLETE":
            order.status = "FAILED"
            order.raw_response = status_json
            order.save(update_fields=["status", "raw_response"])
            return Response(
                {"message": "Payment verification failed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        order.status = "PAID"
        order.esewa_ref_id = status_json.get("ref_id") or status_json.get("refId")
        order.esewa_transaction_code = transaction_code
        order.raw_response = {
            "decoded_response": decoded_data,
            "status_check": status_json,
        }
        order.save()

        # optional stock update
        for order_item in order.items.select_related("product"):
            product = order_item.product
            if product.stock >= order_item.quantity:
                product.stock -= order_item.quantity
                product.save(update_fields=["stock"])

        CartItem.objects.filter(user=request.user).delete()

        return Response(
            {
                "message": "Payment verified successfully.",
                "transaction_uuid": order.transaction_uuid,
                "ref_id": order.esewa_ref_id,
            },
            status=status.HTTP_200_OK,
        )