from django.urls import path
from .views import PlaceOrderAPIView, SelectPaymentMethodAPIView, OrderListAPIView, UpdateOrderStatusAPIView

urlpatterns = [
    # Order-related endpoints
    path('order/place/', PlaceOrderAPIView.as_view(), name='place_order'),
    path('order/select-payment/', SelectPaymentMethodAPIView.as_view(), name='select_payment_method'),
    path('order/list/', OrderListAPIView.as_view(), name='order_list'),
    
    # Admin-related endpoints (for updating order status)
    path('order/update-status/<int:order_id>/', UpdateOrderStatusAPIView.as_view(), name='update_order_status'),
]
