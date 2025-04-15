from rest_framework.views import APIView
from django.conf import settings
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, serializers
from .models import Order, OrderItem
from cart.models import Cart, CartItem
from .serializers import *
from chargily_pay import ChargilyClient
from chargily_pay.entity import Customer, Address, Product, Price, PaymentLink, PaymentItem
from drf_yasg.utils import swagger_auto_schema

from decimal import Decimal

# Chargily configuration
chargily = ChargilyClient(
    secret=settings.CHARGILY_SECRET,
    key=settings.CHARGILY_KEY,
    url=settings.CHARGILY_URL,
)



class PlaceOrderAPIView(APIView):
    """Create an order from the selected cart items and initiate payment"""
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Place a new order from selected cart items.",
        responses={201: OrderSerializer()}
    )
    def post(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)

        selected_items = cart.items.filter(selected=True)

        if not selected_items.exists():
            return Response({"error": "No items selected for checkout"}, status=status.HTTP_400_BAD_REQUEST)

        total_price = sum(Decimal(item.total_price()) for item in selected_items)

        # Create the order
        order = Order.objects.create(user=request.user, total_price=total_price, status="pending")

        # Create order items
        order_items = [
            OrderItem(
                order=order,
                product_name=item.product_detail.product.name,
                quantity=item.quantity,
                price=item.total_price()
            )
            for item in selected_items
        ]
        OrderItem.objects.bulk_create(order_items)

        # Clear the selected items from the cart
        selected_items.delete()

        return Response({
            "order": OrderSerializer(order).data,
            "message": "Order created successfully. Please select your payment method."
        }, status=status.HTTP_201_CREATED)


class SelectPaymentMethodAPIView(APIView):
    """Select payment method after placing an order"""
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=PaymentMethodSerializer,
        operation_description="Choose payment method: 'cod' or 'online'.",
    )
    def post(self, request):
        serializer = PaymentMethodSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        order_id = serializer.validated_data["order_id"]
        payment_method = serializer.validated_data["payment_method"]

        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        if payment_method == "cod":
            order.status = "pending"
            order.save()

            return Response({
                "message": "Your order is pending. You will receive a call from the admin for confirmation."
            })

        elif payment_method == "online":
            customer = Customer(
                name=request.user.username,
                email=request.user.email,
                address=Address(address="User Address", state="State", country="dz")  # You can customize this
            )
            customer_response = chargily.create_customer(customer)

            product = Product(
                name=f"Order #{order.id}",
                description=f"Order description for ID {order.id}"
            )
            product_response = chargily.create_product(product)
            product_id = product_response["id"]

            price = Price(
                amount=int(order.total_price * 100),  # cents
                currency="dzd",
                product_id=product_id
            )
            price_response = chargily.create_price(price)
            price_id = price_response["id"]

            checkout = PaymentLink(
                name=f"Payment link for Order #{order.id}",
                items=[PaymentItem(price=price_id, quantity=1)]
            )
            payment_link_response = chargily.create_payment_link(checkout)

            return Response({
                "message": "Proceed to payment.",
                "payment_url": payment_link_response.get("url")
            })

        return Response({"error": "Invalid payment method selected"}, status=status.HTTP_400_BAD_REQUEST)


class OrderListAPIView(APIView):
    """List all orders for the logged-in user"""
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="List all orders for the current user.",
        responses={200: OrderSerializer(many=True)}
    )
    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
