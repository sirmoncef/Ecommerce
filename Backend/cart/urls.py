from django.urls import path
from .views import *

urlpatterns = [
    path("cart/", CartAPIView.as_view(), name="cart"),
    path("cart/add/", AddToCartAPIView.as_view(), name="add_to_cart"),
    path("cart/update/<int:item_id>/", UpdateCartItemAPIView.as_view(), name="update_cart_item"),
    path("cart/delete/<int:item_id>/", DeleteCartItemAPIView.as_view(), name="delete_cart_item"),
    path("cart/select/<int:item_id>/", SelectCartItemAPIView.as_view(), name="select_cart_item"),
]
