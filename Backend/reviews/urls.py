from django.urls import path
from .views import ReviewListCreateAPIView, ReviewDetailAPIView

urlpatterns = [
    
    path("reviews/product/<int:product_id>/", ReviewListCreateAPIView.as_view(), name="review-list"),

    
    path("reviews/<int:review_id>/", ReviewDetailAPIView.as_view(), name="review-detail"),
]
