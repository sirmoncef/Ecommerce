from django.db import models
from django.conf import settings
from products.models import ProductDetail

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart")

    def total_price(self):
        """Calculate total price for only selected items"""
        return sum(item.total_price() for item in self.items.filter(selected=True))

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product_detail = models.ForeignKey(ProductDetail, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    selected = models.BooleanField(default=True)  # ✅ Tracks if the item is selected

    def total_price(self):
        """Total price for this item"""
        return self.product_detail.product.calculate_discount() * self.quantity
