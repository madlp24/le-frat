from django import forms
from .models import ProductReview

class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ("rating", "comment", "image")
        widgets = {
            "comment": forms.Textarea(attrs={"rows": 4, "placeholder": "Sin tanta vuelta… ¿qué tal estuvo?"}),
        }
