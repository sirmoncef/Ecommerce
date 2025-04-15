from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Review
from products.models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated ,AllowAny
from drf_yasg.utils import swagger_auto_schema

class ReviewListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve all reviews for a specific product",
        responses={200: ReviewSerializer(many=True)}
    )
    def get(self, request, product_id):
        reviews = Review.objects.filter(product_id=product_id)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=ReviewSerializer,
        operation_description="Create a review for a product",
        responses={
            201: ReviewSerializer(),
            400: "You have already reviewed this product or invalid input"
        }
    )
    def post(self, request, product_id, *args, **kwargs):  
        product = get_object_or_404(Product, id=product_id)

        if Review.objects.filter(user=request.user, product=product).exists():
            return Response({"error": "You have already reviewed this product"}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        data["product_id"] = product_id
        serializer = ReviewSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user, product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ReviewDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve a review by its ID",
        responses={200: ReviewSerializer()}
    )
    def get(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=ReviewSerializer,
        operation_description="Update a review",
        responses={200: ReviewSerializer(), 400: "Invalid input"}
    )
    def put(self, request, review_id):
        review = get_object_or_404(Review, id=review_id, user=request.user)
        serializer = ReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a review by its ID",
        responses={204: "Review deleted successfully"}
    )
    def delete(self, request, review_id):
        review = get_object_or_404(Review, id=review_id, user=request.user)
        review.delete()
        return Response({"message": "Review deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
