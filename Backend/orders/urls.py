from django.urls import path
from .views import PlaceOrderAPIView, SelectPaymentMethodAPIView, OrderListAPIView

urlpatterns = [
    # Order-related endpoints
    path('order/place/', PlaceOrderAPIView.as_view(), name='place_order'),
    path('order/select-payment/', SelectPaymentMethodAPIView.as_view(), name='select_payment_method'),
    path('order/list/', OrderListAPIView.as_view(), name='order_list'),
    
   
]
