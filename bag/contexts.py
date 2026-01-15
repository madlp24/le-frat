from decimal import Decimal
from products.models import Product

def bag_contents(request):
    bag = request.session.get("bag", {})
    bag_items = []
    total = Decimal("0.00")
    product_count = 0

    products = Product.objects.filter(id__in=bag.keys())

    for product in products:
        qty = bag.get(str(product.id), 0)
        line_total = product.price * qty
        total += line_total
        product_count += qty
        bag_items.append({
            "product": product,
            "quantity": qty,
            "line_total": line_total,
        })

    return {
        "bag_items": bag_items,
        "total": total,
        "product_count": product_count,
    }
