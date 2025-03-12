from django.urls import path
from .views import *
urlpatterns = [
    # Category URLs
    path("categories/", CategoryAPIView.as_view(), name="categories"),
    path("categories/<int:pk>/", CategoryAPIView.as_view(), name="category-detail"),

    # Brand URLs
    path("brands/", BrandAPIView.as_view(), name="brands"),
    path("brands/<int:pk>/", BrandAPIView.as_view(), name="brand-detail"),

    # Product URLs
    path("products/", ProductAPIView.as_view(), name="products"),
    path("products/<int:pk>/", ProductAPIView.as_view(), name="product-detail"),

    # Attribute URLs
    path("attributes/", AttributeAPIView.as_view(), name="attributes"),
    path("attributes/<int:pk>/", AttributeAPIView.as_view(), name="attribute-detail"),

    # Product Detail URLs
    path("product-details/", ProductDetailAPIView.as_view(), name="product-details"),
    path("product-details/<int:pk>/", ProductDetailAPIView.as_view(), name="product-detail-detail"),

    # Available Product Details (Only products with stock > 0)
    path("product-details/available/", AvailableProductDetailAPIView.as_view(), name="available-products"),
]
