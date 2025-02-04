from django.urls import path
from .views import CartAPIView, AddToCartAPIView, UpdateCartItemAPIView, RemoveFromCartAPIView

urlpatterns = [
    path("cart/", CartAPIView.as_view(), name="cart-view"),
    path("cart/add/", AddToCartAPIView.as_view(), name="cart-add"),
    path("cart/update/<int:item_id>/", UpdateCartItemAPIView.as_view(), name="cart-update"),
    path("cart/remove/<int:item_id>/", RemoveFromCartAPIView.as_view(), name="cart-remove"),
]
