from django.shortcuts import render
from products.models import Product

def index(request):
    featured_skus = ["LF-HOOD-001", "LF-TEE-004", "LF-ACC-004"]  # hoodie, tee, cap/hat

    featured_products = list(Product.objects.filter(sku__in=featured_skus))

    sku_to_image = {
        "LF-HOOD-001": "drop-hoodie.jpg",
        "LF-TEE-004": "drop-tshirt.jpg",
        "LF-ACC-004": "drop-cap.jpg",
    }

    for p in featured_products:
        p.home_image = sku_to_image.get(p.sku, "drop-default.jpg")

    order_map = {sku: i for i, sku in enumerate(featured_skus)}
    featured_products.sort(key=lambda p: order_map.get(p.sku, 999))

    return render(request, "home/index.html", {"featured_products": featured_products})
