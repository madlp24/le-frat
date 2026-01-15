# checkout/models.py
import uuid
from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Order(models.Model):
    order_number = models.CharField(max_length=32, unique=True, editable=False)

    user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL
    )

    full_name = models.CharField(max_length=80)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)

    street_address1 = models.CharField(max_length=80)
    street_address2 = models.CharField(max_length=80, blank=True)
    town_or_city = models.CharField(max_length=40)
    postcode = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=40)

    date = models.DateTimeField(auto_now_add=True)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.order_number

    def _generate_order_number(self):
        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)


class OrderLineItem(models.Model):
    order = models.ForeignKey(
        Order, related_name="lineitems", on_delete=models.CASCADE
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    lineitem_total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
