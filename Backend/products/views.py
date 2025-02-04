from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from django.shortcuts import get_object_or_404

from .models import Product, ProductImage, ProductAttribute
from .serializers import ProductSerializer, ProductImageSerializer, ProductAttributeSerializer

class ProductPagination(PageNumberPagination):
    """Pagination for products (10 per page)."""
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50

class ProductListCreateAPIView(ListAPIView, APIView):
    """
    GET: List all products with search, filtering, and pagination.
    POST: Create a new product.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["category", "brand"]  # Filtering by category & brand
    search_fields = ["name", "description"]  # Search by name or description

    def post(self, request):
        """Create a new product"""
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetailAPIView(APIView):
    """
    GET: Retrieve a product.
    PUT: Update a product.
    DELETE: Delete a product.
    """

    def get(self, request, pk):
        """Retrieve a single product"""
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """Update a product"""
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            product = serializer.save()
            return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Delete a product"""
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response({"message": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class ProductImageListCreateAPIView(APIView):
    """
    POST: Add an image to a product.
    """

    def post(self, request, product_id):
        """Add an image to a product"""
        data = request.data.copy()
        data["product"] = product_id
        serializer = ProductImageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductAttributeListCreateAPIView(APIView):
    """
    POST: Add an attribute (e.g., size, color) to a product.
    """

    def post(self, request, product_id):
        """Add an attribute to a product"""
        data = request.data.copy()
        data["product"] = product_id
        serializer = ProductAttributeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
