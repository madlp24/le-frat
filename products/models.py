from django.db import models
from django.core.validators import MinValueValidator

class Category(models.Model):
    name = models.SlugField(max_length=40, unique=True)
    friendly_name = models.CharField(max_length=60)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.friendly_name


class Product(models.Model):
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL, related_name="products"
    )
    sku = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=80)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0.01)])
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="products/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
