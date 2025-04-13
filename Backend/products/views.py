from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import *
from .serializers import *


class CategoryAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            category = get_object_or_404(Category, pk=pk)
            serializer = CategorySerializer(category)
        else:
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class BrandAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            brand = get_object_or_404(Brand, pk=pk)
            serializer = BrandSerializer(brand)
        else:
            brands = Brand.objects.all()
            serializer = BrandSerializer(brands, many=True)
        return Response(serializer.data)

    


class ProductAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            product = get_object_or_404(Product, pk=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        
      
        category_name = request.GET.get('category', None)
        brand_name = request.GET.get('brand', None)
        product_name = request.GET.get('name', None)
        
        
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

    


class AttributeAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            attribute = get_object_or_404(Attribute, pk=pk)
            serializer = AttributeSerializer(attribute)
        else:
            attributes = Attribute.objects.all()
            serializer = AttributeSerializer(attributes, many=True)
        return Response(serializer.data)

    


class ProductDetailAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            product_detail = get_object_or_404(ProductDetail, pk=pk)
            serializer = ProductDetailSerializer(product_detail)
        else:
            product_details = ProductDetail.objects.all()
            serializer = ProductDetailSerializer(product_details, many=True)
        return Response(serializer.data)

    

   
class AvailableProductDetailAPIView(APIView):
    def get(self, request):
        available_products = ProductDetail.objects.filter(stock__gt=0)
        serializer = ProductDetailSerializer(available_products, many=True)
        return Response(serializer.data)