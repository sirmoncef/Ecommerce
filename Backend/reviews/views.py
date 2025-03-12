from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Review
from products.models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated ,AllowAny

class ReviewListCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]


    def get(self, request, product_id):
        """Retrieve all reviews for a specific product"""
        reviews = Review.objects.filter(product_id=product_id)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, product_id, *args, **kwargs):  # ✅ Get product_id from URL
        """Create a review for a product"""
        product = get_object_or_404(Product, id=product_id)  # ✅ Ensure product exists

        # Check if user has already reviewed the product
        if Review.objects.filter(user=request.user, product=product).exists():
            return Response({"error": "You have already reviewed this product"}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ Ensure product_id is added to validated data
        data = request.data.copy()  # Copy request data
        data["product_id"] = product_id  # Add product_id to request data

        serializer = ReviewSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user, product=product)  # ✅ Assign user and product
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewDetailAPIView(APIView):
   

    def get(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, review_id):
        """Update a review"""
        review = get_object_or_404(Review, id=review_id, user=request.user)
        serializer = ReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, review_id):
        """Delete a review"""
        review = get_object_or_404(Review, id=review_id, user=request.user)
        review.delete()
        return Response({"message": "Review deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
