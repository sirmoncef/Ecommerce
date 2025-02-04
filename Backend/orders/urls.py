from django.urls import path
from .views import *

urlpatterns = [
    path("orders/", OrderListAPIView.as_view(), name="order-list"),
    path("orders/place/", PlaceOrderAPIView.as_view(), name="order-place"),
    path("orders/<int:order_id>/", OrderDetailAPIView.as_view(), name="order-detail"),
    path("orders/<int:order_id>/update-status/", UpdateOrderStatusAPIView.as_view(), name="order-update-status"),
]
