from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import *
from .serializers import *
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class CategoryAPIView(APIView):

    @swagger_auto_schema(
        operation_description="Retrieve all categories or a specific one by ID",
        responses={200: CategorySerializer(many=True)}
    )
    def get(self, request, pk=None):
        if pk:
            category = get_object_or_404(Category, pk=pk)
            serializer = CategorySerializer(category)
        else:
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class BrandAPIView(APIView):

    @swagger_auto_schema(
        operation_description="Retrieve all brands or a specific one by ID",
        responses={200: BrandSerializer(many=True)}
    )
    def get(self, request, pk=None):
        if pk:
            brand = get_object_or_404(Brand, pk=pk)
            serializer = BrandSerializer(brand)
        else:
            brands = Brand.objects.all()
            serializer = BrandSerializer(brands, many=True)
        return Response(serializer.data)


    


class ProductAPIView(APIView):

    @swagger_auto_schema(
        operation_description="Retrieve all products with optional filtering by category, brand, or name",
        manual_parameters=[
            openapi.Parameter('category', openapi.IN_QUERY, description="Category name", type=openapi.TYPE_STRING),
            openapi.Parameter('brand', openapi.IN_QUERY, description="Brand name", type=openapi.TYPE_STRING),
            openapi.Parameter('name', openapi.IN_QUERY, description="Product name", type=openapi.TYPE_STRING),
        ],
        responses={200: ProductSerializer(many=True)}
    )
    def get(self, request):
        category_name = request.GET.get('category')
        brand_name = request.GET.get('brand')
        product_name = request.GET.get('name')

        filters = Q()
        if category_name:
            filters &= Q(category__name__icontains=category_name)
        if brand_name:
            filters &= Q(brand__name__icontains=brand_name)
        if product_name:
            filters &= Q(name__icontains=product_name)

        products = Product.objects.filter(filters)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)



class ProductOverviewAPIView(APIView):

    @swagger_auto_schema(
        operation_description="Retrieve product details by ID. ID is required.",
        responses={
            200: ProductDetailSerializer(),
            400: 'Bad Request: Product ID is required.'
        }
    )
    def get(self, request, pk=None):
        if not pk:
            return Response(
                {"error": "Product ID is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        product_detail = get_object_or_404(ProductDetail, pk=pk)
        serializer = ProductDetailSerializer(product_detail)
        return Response(serializer.data)
    


class AttributeAPIView(APIView):

    @swagger_auto_schema(
        operation_description="Retrieve all attributes or a specific one by ID",
        responses={200: AttributeSerializer(many=True)}
    )
    def get(self, request, pk=None):
        if pk:
            attribute = get_object_or_404(Attribute, pk=pk)
            serializer = AttributeSerializer(attribute)
        else:
            attributes = Attribute.objects.all()
            serializer = AttributeSerializer(attributes, many=True)
        return Response(serializer.data)



class AvailableProductDetailAPIView(APIView):

    @swagger_auto_schema(
        operation_description="Retrieve only available products (stock > 0)",
        responses={200: ProductDetailSerializer(many=True)}
    )
    def get(self, request):
        available_products = ProductDetail.objects.filter(stock__gt=0)
        serializer = ProductDetailSerializer(available_products, many=True)
        return Response(serializer.data)
