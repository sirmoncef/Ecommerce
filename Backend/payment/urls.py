from django.urls import path
from .views import create_payment, payment_list, payment_detail, payment_webhook  # Ensure this is correct

urlpatterns = [
    path('create/', create_payment, name='create_payment'),
    path('list/', payment_list, name='payment_list'),
    path('detail/<str:transaction_id>/', payment_detail, name='payment_detail'),
    path('webhook/', payment_webhook, name='payment_webhook'),  # Ensure this path exists
]
