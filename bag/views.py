from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from products.models import Product


def view_bag(request):
    """Display the shopping bag contents."""
    bag = request.session.get("bag", {})
    return render(request, "bag/bag.html", {"bag": bag})


def add_to_bag(request, product_id):
    """Add a quantity of the specified product to the shopping bag."""
    product = get_object_or_404(Product, pk=product_id)

    try:
        quantity = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        quantity = 1

    if quantity < 1:
        messages.error(request, "Please choose a valid quantity.")
        return redirect("product_detail", product_id=product.id)

    bag = request.session.get("bag", {})

    product_id_str = str(product_id)
    if product_id_str in bag:
        bag[product_id_str] += quantity
        messages.success(request, f"Updated {product.name} quantity in your bag.")
    else:
        bag[product_id_str] = quantity
        messages.success(request, f"Added {product.name} to your bag.")

    request.session["bag"] = bag
    return redirect("view_bag")
