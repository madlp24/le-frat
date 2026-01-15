from decimal import Decimal
from products.models import Product


def bag_contents(request):
    bag = request.session.get("bag", {})
    bag_items = []
    total = Decimal("0.00")
    product_count = 0

    for item_id, quantity in bag.items():
        product = Product.objects.get(pk=item_id)
        line_total = product.price * quantity

        total += line_total
        product_count += quantity

        bag_items.append({
            "product": product,
            "quantity": quantity,
            "line_total": line_total,
        })

    return {
        "bag_items": bag_items,
        "total": total,
        "product_count": product_count,
    }
