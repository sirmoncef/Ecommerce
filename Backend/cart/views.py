from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from products.models import ProductDetail
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class CartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve all items in the user's cart along with total price.",
        responses={200: CartSerializer()}
    )
    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class AddToCartAPIView(APIView):
    """Add an item to the cart"""
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Add a product to the user's cart. If the product is already in the cart, it updates the quantity.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['product_detail_id'],
            properties={
                'product_detail_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the product detail'),
                'quantity': openapi.Schema(type=openapi.TYPE_INTEGER, description='Quantity to add', default=1),
            }
        ),
        responses={201: CartItemSerializer(), 404: 'Product not found'}
    )
    def post(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        product_detail_id = request.data.get("product_detail_id")
        quantity = request.data.get("quantity", 1)

        if not isinstance(quantity, int) or quantity < 1:
            return Response({"error": "Quantity must be a positive integer."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product_detail = ProductDetail.objects.get(id=product_detail_id)
        except ProductDetail.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product_detail=product_detail)
        if created:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity
        cart_item.save()

        return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)


class UpdateCartItemAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Update the quantity of a cart item.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'quantity': openapi.Schema(type=openapi.TYPE_INTEGER, description='New quantity'),
            }
        ),
        responses={200: CartItemSerializer(), 404: 'Item not found'}
    )
    def patch(self, request, item_id):
        try:
            cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        quantity = request.data.get("quantity")
        if quantity is not None:
            if not isinstance(quantity, int) or quantity < 1:
                return Response({"error": "Quantity must be a positive integer."}, status=status.HTTP_400_BAD_REQUEST)
            cart_item.quantity = quantity
            cart_item.save()

        return Response(CartItemSerializer(cart_item).data)


class DeleteCartItemAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Remove a cart item by its ID.",
        responses={
            204: openapi.Response(description="Item removed successfully"),
            404: "Item not found"
        }
    )
    def delete(self, request, item_id):
        try:
            cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
            cart_item.delete()
            return Response({"message": "Item removed from cart"}, status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)


class SelectCartItemAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Update the selected status of a cart item.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'selected': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='True to select, False to unselect'),
            }
        ),
        responses={
            200: openapi.Response(description="Item selection updated"),
            404: "Item not found"
        }
    )
    def patch(self, request, item_id):
        try:
            cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
            selected = request.data.get("selected")
            if isinstance(selected, bool):
                cart_item.selected = selected
                cart_item.save()
                return Response({"message": "Item selection updated."})
            return Response({"error": "Selected must be a boolean."}, status=status.HTTP_400_BAD_REQUEST)
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found."}, status=status.HTTP_404_NOT_FOUND)
