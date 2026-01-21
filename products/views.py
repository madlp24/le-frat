from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category
from .forms import ProductForm

def is_admin(user):
    return user.is_staff

def product_list(request):
    products = Product.objects.all().order_by("-created_at")
    categories = Category.objects.all()

    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()
    sort = request.GET.get("sort", "").strip()

    # Search
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    # Filter by category (we use category.name which is your SlugField)
    if category:
        products = products.filter(category__name=category)

    # Sort
    if sort == "price_asc":
        products = products.order_by("price")
    elif sort == "price_desc":
        products = products.order_by("-price")
    elif sort == "name_asc":
        products = products.order_by("name")
    elif sort == "name_desc":
        products = products.order_by("-name")

    context = {
        "products": products,
        "categories": categories,
        "search_term": query,
        "selected_category": category,
        "selected_sort": sort,
    }
    return render(request, "products/products.html", context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))

    return render(request, "products/product_detail.html", {"product": product})

@login_required
@user_passes_test(is_admin)
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully.")
            return redirect("products")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProductForm()

    return render(request, "products/product_form.html", {
        "form": form,
        "product": None,   
    })

@login_required
@user_passes_test(is_admin)
def edit_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully.")
            return redirect("products")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProductForm(instance=product)

    return render(request, "products/product_form.html", {
        "form": form,
        "product": product
    })

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    # Optional but recommended (staff-only)
    if not request.user.is_staff:
        messages.error(request, "Sorry, only store owners can do that.")
        return redirect("products")

    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted.")
        return redirect("products")

    return render(request, "products/product_confirm_delete.html", {"product": product})
