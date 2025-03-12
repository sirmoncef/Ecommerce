from django.db import models
from decimal import Decimal

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)
    logo = models.ImageField(upload_to="brands/", blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, related_name="products")
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def calculate_discount(self):
        if self.discount > 0:
            return self.price * Decimal(self.discount / 100)  # Ensure the discount is a Decimal
        return self.price




class Attribute(models.Model):
    
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name="values")
    value = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"


class ProductDetail(models.Model):
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="details")
    attributes = models.ManyToManyField(AttributeValue, related_name="details")
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} - {', '.join([str(attr) for attr in self.attributes.all()])}"

    def is_available(self):
        
        return self.stock > 0
