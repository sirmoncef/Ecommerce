from rest_framework import serializers
from .models import Review
from products.serializers import *

class ReviewSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Review
        fields = ["id", "user", "product", "product_id", "rating", "comment", "created_at", "updated_at"]
