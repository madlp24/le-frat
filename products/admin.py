from django.contrib import admin
from .models import Product, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("friendly_name", "name")
    search_fields = ("friendly_name", "name")
    ordering = ("friendly_name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "sku",
        "category",
        "price",
        "stock",
        "has_image",
        "created_at",
    )
    list_filter = ("category", "created_at")
    search_fields = ("name", "description", "sku")
    ordering = ("-created_at",)
    list_per_page = 25
    autocomplete_fields = ("category",)
    readonly_fields = ("created_at",)

    def has_image(self, obj):
        return bool(obj.image)
    has_image.boolean = True
    has_image.short_description = "Image?"
