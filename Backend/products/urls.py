from django.urls import path
from .views import *

urlpatterns = [
    path("products/", ProductListCreateAPIView.as_view(), name="product-list-create"),  # List & Create
    path("products/<int:pk>/", ProductDetailAPIView.as_view(), name="product-detail"),  # Retrieve, Update, Delete
    path("products/<int:product_id>/images/", ProductImageListCreateAPIView.as_view(), name="product-image-create"),  # Add Images
    path("products/<int:product_id>/attributes/", ProductAttributeListCreateAPIView.as_view(), name="product-attribute-create"),  # Add Attributes
]
