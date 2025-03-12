from rest_framework import serializers
from .models import Cart, CartItem

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product_detail.product.name", read_only=True)
    price = serializers.DecimalField(source="product_detail.product.calculate_discount", max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = CartItem
        fields = ["id", "product_name", "quantity", "price", "selected"]

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id", "items", "total_price"]

    def get_total_price(self, obj):
        return obj.total_price()
