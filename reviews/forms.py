from django import forms
from .models import ProductReview

class ProductReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")],
        initial=5,
        widget=forms.Select(attrs={"class": "form-select"})
    )

    class Meta:
        model = ProductReview
        fields = ("rating", "comment", "image")
        widgets = {
            "comment": forms.Textarea(attrs={
                "rows": 4,
                "class": "form-control",
                "placeholder": "No fluff… how was it?"
            }),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
