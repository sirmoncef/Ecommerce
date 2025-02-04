from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Order, OrderItem
from cart.models import Cart, CartItem
from .serializers import OrderSerializer
from django.contrib.auth.models import User

class OrderListAPIView(APIView):
   
    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PlaceOrderAPIView(APIView):
   

    def post(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        if not cart.items.exists():
            return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        # Create Order
        order = Order.objects.create(user=request.user)

        # Move Cart Items to Order Items
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
            )

        # Clear the cart
        cart.items.all().delete()

        return Response({"message": "Order placed successfully", "order_id": order.id}, status=status.HTTP_201_CREATED)

class OrderDetailAPIView(APIView):
   

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, order_id):
        """Cancel an order"""
        order = get_object_or_404(Order, id=order_id, user=request.user)
        if order.status == "pending":
            order.status = "canceled"
            order.save()
            return Response({"message": "Order canceled"}, status=status.HTTP_200_OK)
        return Response({"error": "Order cannot be canceled"}, status=status.HTTP_400_BAD_REQUEST)

class UpdateOrderStatusAPIView(APIView):
   
    def put(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        if not request.user.is_staff:  # Ensure only admins can update
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        new_status = request.data.get("status")
        if new_status in ["pending", "completed", "canceled"]:
            order.status = new_status
            order.save()
            return Response({"message": "Order status updated"}, status=status.HTTP_200_OK)

        return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)
