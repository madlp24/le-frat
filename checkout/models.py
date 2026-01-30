# checkout/models.py
import uuid
from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from decimal import Decimal
from django.conf import settings
from django.db.models import Sum


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

    # Totals
    order_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    delivery_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Stripe + bag snapshot
    original_bag = models.TextField(blank=True, null=True)
    stripe_pid = models.CharField(max_length=254, blank=True, null=True)

    def __str__(self):
        return self.order_number

    def _generate_order_number(self):
        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def update_total(self):
        self.order_total = self.lineitems.aggregate(
            Sum('lineitem_total')
        )['lineitem_total__sum'] or Decimal("0.00")

        percentage = Decimal(getattr(settings, "STANDARD_DELIVERY_PERCENTAGE", 0)) / Decimal("100")
        self.delivery_cost = (self.order_total * percentage).quantize(Decimal("0.01"))
        self.grand_total = (self.order_total + self.delivery_cost).quantize(Decimal("0.01"))

        self.save(update_fields=["order_total", "delivery_cost", "grand_total"])




class OrderLineItem(models.Model):
    order = models.ForeignKey(
        Order,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='lineitems'
    )
    product = models.ForeignKey(
        Product,
        null=False,
        blank=False,
        on_delete=models.CASCADE
    )
    quantity = models.IntegerField(default=0)
    lineitem_total = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        editable=False
    )

    def save(self, *args, **kwargs):
        self.lineitem_total = (self.product.price * self.quantity).quantize(Decimal("0.01"))
        super().save(*args, **kwargs)
        self.order.update_total()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.order.update_total()

    def __str__(self):
        return f'SKU {self.product.sku} on order {self.order.order_number}'
