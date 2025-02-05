from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Review
from products.models import *
from .serializers import *

class ReviewListCreateAPIView(APIView):
   

    def get(self, request, product_id):
        reviews = Review.objects.filter(product_id=product_id)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Create a review for a product"""
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            product = get_object_or_404(Product, id=request.data["product_id"])

            # Check if user already reviewed the product
            if Review.objects.filter(user=request.user, product=product).exists():
                return Response({"error": "You have already reviewed this product"}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save(user=request.user, product=product)
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
