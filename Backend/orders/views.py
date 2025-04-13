from rest_framework.views import APIView
from django.conf import settings
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from .models import Order, OrderItem
from cart.models import Cart, CartItem
from .serializers import OrderSerializer
from chargily_pay import ChargilyClient
from chargily_pay.entity import Customer, Address, Product, Price, PaymentLink, PaymentItem

chargily = ChargilyClient(
    secret=settings.CHARGILY_SECRET,
    key=settings.CHARGILY_KEY,
    url=settings.CHARGILY_URL,
)

class PlaceOrderAPIView(APIView):
    """Create an order from the selected cart items and initiate payment"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = Cart.objects.get(user=request.user)
        selected_items = cart.items.filter(selected=True)

        if not selected_items.exists():
            return Response({"error": "No items selected for checkout"}, status=status.HTTP_400_BAD_REQUEST)

        total_price = sum(item.total_price() for item in selected_items)

        # Create the order
        order = Order.objects.create(user=request.user, total_price=total_price, status="pending")

        # Create order items
        order_items = [
            OrderItem(order=order, product_name=item.product_detail.product.name, quantity=item.quantity, price=item.total_price())
            for item in selected_items
        ]
        OrderItem.objects.bulk_create(order_items)

        # Clear the cart after order is placed
        selected_items.delete()

        return Response({
            "order": OrderSerializer(order).data,
            "message": "Order created successfully. Please select your payment method."
        }, status=status.HTTP_201_CREATED)

class SelectPaymentMethodAPIView(APIView):
    """Select payment method after placing an order"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order_id = request.data.get("order_id")
        payment_method = request.data.get("payment_method")  # 'cod' or 'online'

        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        if payment_method == "cod":
            # If COD is selected, set the order status to 'pending' and notify the admin
            order.status = "pending"
            order.save()

            # Respond with confirmation
            return Response({
                "message": "Your order is pending. You will receive a call from the admin for confirmation."
            })

        elif payment_method == "online":
            # Generate the online payment link using Chargily
            # Create Customer for payment
            customer = Customer(
                name=request.user.username,
                email=request.user.email,
                address=Address(address="User Address", state="State", country="dz"),  # Replace with actual address info
            )
            customer_response = chargily.create_customer(customer)

            # Create Product for payment
            product = Product(name="Order #" + str(order.id), description="Order description for ID " + str(order.id))
            product_response = chargily.create_product(product)
            product_id = product_response["id"]

            # Create Price for payment
            price = Price(
                amount=int(order.total_price * 100),  # Convert to cents
                currency="dzd",  # Currency code
                product_id=product_id,  # Link price to product
            )
            price_response = chargily.create_price(price)
            price_id = price_response["id"]

            # Create Checkout for payment
            checkout = PaymentLink(
                name="Payment link for Order #" + str(order.id),
                items=[PaymentItem(price=price_id, quantity=1)]
            )
            payment_link_response = chargily.create_payment_link(checkout)

            # Return the payment URL for the user to proceed
            return Response({
                "message": "Proceed to payment.",
                "payment_url": payment_link_response.get("url")
            })

        else:
            return Response({"error": "Invalid payment method selected"}, status=status.HTTP_400_BAD_REQUEST)

class OrderListAPIView(APIView):
    """List all orders for the logged-in user"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


