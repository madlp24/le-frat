from django import forms
from django.core.exceptions import ValidationError
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Better UX: placeholders + HTML validation (client-side)
        self.fields["sku"].widget.attrs.update({"required": True, "maxlength": 20})
        self.fields["name"].widget.attrs.update({"required": True, "maxlength": 80})
        self.fields["description"].widget.attrs.update({"required": True})
        self.fields["price"].widget.attrs.update({"required": True, "min": "0.01", "step": "0.01"})
        self.fields["stock"].widget.attrs.update({"required": True, "min": "0"})

    # Prevent whitespace-only SKU
    def clean_sku(self):
        sku = (self.cleaned_data.get("sku") or "").strip()
        if not sku:
            raise ValidationError("SKU cannot be blank.")
        if " " in sku:
            raise ValidationError("SKU cannot contain spaces.")
        return sku

    # Prevent whitespace-only name
    def clean_name(self):
        name = (self.cleaned_data.get("name") or "").strip()
        if not name:
            raise ValidationError("Product name cannot be blank.")
        return name

    # Prevent whitespace-only description
    def clean_description(self):
        description = (self.cleaned_data.get("description") or "").strip()
        if not description:
            raise ValidationError("Description cannot be blank.")
        return description

    # Price must be > 0
    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is None:
            raise ValidationError("Price is required.")
        if price <= 0:
            raise ValidationError("Price must be greater than 0.")
        return price

    # Stock must be >= 0 (PositiveIntegerField already helps, but we keep a clear message)
    def clean_stock(self):
        stock = self.cleaned_data.get("stock")
        if stock is None:
            raise ValidationError("Stock is required.")
        if stock < 0:
            raise ValidationError("Stock cannot be negative.")
        return stock
