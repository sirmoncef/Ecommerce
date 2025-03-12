from django.urls import path
from .views import *

urlpatterns = [
    path("order/place/", PlaceOrderAPIView.as_view(), name="place_order"),
    path("order/list/", OrderListAPIView.as_view(), name="order_list"),
    path("order/<int:order_id>/", OrderDetailAPIView.as_view(), name="order_detail"),
    path("order/<int:order_id>/cancel/", CancelOrderAPIView.as_view(), name="cancel_order"),
    path("order/<int:order_id>/update-status/", UpdateOrderStatusAPIView.as_view(), name="update_order_status"),
]
