from django.contrib import admin
from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)  # Added search_fields


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "logo")
    search_fields = ("name",)  # Added search_fields


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "stock_count", "category", "brand", "created_at")
    list_filter = ("category", "brand")
    search_fields = ("name", "description")
    autocomplete_fields = ("category", "brand")  # Fixed error

    def stock_count(self, obj):
        """Calculate total stock from ProductDetail."""
        return obj.details.aggregate(models.Sum("stock"))["stock__sum"] or 0

    stock_count.short_description = "Stock"  # Custom name in the admin panel


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ("attribute", "value")


@admin.register(ProductDetail)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ("product", "get_attributes", "stock")

    def get_attributes(self, obj):
        """Display attribute values as a comma-separated list."""
        return ", ".join([str(attr) for attr in obj.attributes.all()])

    get_attributes.short_description = "Attributes"
