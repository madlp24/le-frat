from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import ProductReview
from .forms import ProductReviewForm
from products.models import Product

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    # Optional: block duplicate if using unique_together
    if ProductReview.objects.filter(product=product, user=request.user).exists():
        messages.warning(request, "You already left a review for this product.")
        return redirect("product_detail", product_id=product.id)

    if request.method == "POST":
        form = ProductReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, "Review added. Thanks for sharing!")

        else:
            messages.error(request, "Please fix the errors in the form.")
    return redirect("product_detail", product_id=product.id)

@login_required
def edit_review(request, review_id):
    review = get_object_or_404(ProductReview, pk=review_id)

    if review.user != request.user and not request.user.is_staff:
        messages.error(request, "You can't edit someone else's review.")
        return redirect("product_detail", product_id=review.product_id)

    if request.method == "POST":
        form = ProductReviewForm(request.POST, request.FILES, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "Review updated.")
            return redirect("product_detail", product_id=review.product_id)
    else:
        form = ProductReviewForm(instance=review)

    return render(request, "reviews/review_form.html", {"form": form, "review": review})

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(ProductReview, pk=review_id)

    if review.user != request.user and not request.user.is_staff:
        messages.error(request, "You can't delete someone else's review.")
        return redirect("product_detail", product_id=review.product_id)

    if request.method == "POST":
        product_id = review.product_id
        review.delete()
        messages.success(request, "Review deleted.")
        return redirect("product_detail", product_id=product_id)

    return render(request, "reviews/review_confirm_delete.html", {"review": review})
