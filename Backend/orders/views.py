from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from .models import Order, OrderItem
from cart.models import Cart, CartItem
from .serializers import OrderSerializer

class PlaceOrderAPIView(APIView):
    """Create an order from the selected cart items"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = Cart.objects.get(user=request.user)
        selected_items = cart.items.filter(selected=True)

        if not selected_items.exists():
            return Response({"error": "No items selected for checkout"}, status=status.HTTP_400_BAD_REQUEST)

        total_price = sum(item.total_price() for item in selected_items)

        # Create the order
        order = Order.objects.create(user=request.user, total_price=total_price)

        # Create order items
        order_items = [
            OrderItem(order=order, product_name=item.product_detail.product.name, quantity=item.quantity, price=item.total_price())
            for item in selected_items
        ]
        OrderItem.objects.bulk_create(order_items)

        # Clear the cart after order is placed
        selected_items.delete()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

class OrderListAPIView(APIView):
    """List all orders for the logged-in user"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

class OrderDetailAPIView(APIView):
    """Get details of a specific order"""
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, user=request.user)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

class CancelOrderAPIView(APIView):
    """Cancel an order if it is still pending"""
    permission_classes = [IsAuthenticated]

    def patch(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, user=request.user)

            if order.status != "pending":
                return Response({"error": "Order cannot be canceled"}, status=status.HTTP_400_BAD_REQUEST)

            order.status = "canceled"
            order.save()

            return Response({"message": "Order canceled successfully"})
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

class UpdateOrderStatusAPIView(APIView):
    """Update order status (Admin only)"""
    permission_classes = [IsAdminUser]

    def patch(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            new_status = request.data.get("status")

            if new_status not in dict(Order.STATUS_CHOICES):
                return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

            order.status = new_status
            order.save()

            return Response({"message": "Order status updated successfully"})
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
