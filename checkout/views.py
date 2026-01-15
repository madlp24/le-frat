import stripe
from decimal import Decimal
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import OrderForm
from .models import Order, OrderLineItem
from django.views.decorators.csrf import csrf_exempt
from products.models import Product
from django.urls import reverse

stripe.api_key = settings.STRIPE_SECRET_KEY



def checkout(request):
    bag = request.session.get("bag", {})

    if not bag:
        messages.error(request, "Your bag is empty.")
        return redirect("products")

    # ---- Calculate total for BOTH GET and POST ----
    total = Decimal("0.00")
    for item_id, quantity in bag.items():
        product = get_object_or_404(Product, pk=item_id)
        total += product.price * quantity

    # Stripe expects an integer in the smallest currency unit (cents)
    stripe_amount = int((total * 100).quantize(Decimal("1")))

    # Create a PaymentIntent on GET (and also available for POST re-render)
    intent = stripe.PaymentIntent.create(
        amount=stripe_amount,
        currency="usd",
    )

    if request.method == "POST":
        form = OrderForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            order.order_total = total
            # If your Order model has these fields, keep them; otherwise remove:
            # order.stripe_pid = intent.id
            # order.original_bag = json.dumps(bag)
            order.save()

            # Create line items
            for item_id, quantity in bag.items():
                product = get_object_or_404(Product, pk=item_id)
                line_total = product.price * quantity

                OrderLineItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    lineitem_total=line_total,
                )

            # Clear bag after order creation (later you can move this to webhook success)
            request.session["bag"] = {}

            messages.success(request, "Order created successfully.")
            return redirect(reverse("checkout_success", args=[order.order_number]))

        messages.error(request, "There was an error with your form.")

    else:
        form = OrderForm()

    context = {
        "order_form": form,
        "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
        "client_secret": intent.client_secret,
        "total": total,  # useful to display on the page
    }
    return render(request, "checkout/checkout.html", context)

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    endpoint_secret = settings.STRIPE_WH_SECRET

    try:
        stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    return HttpResponse(status=200)

def checkout_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    return render(request, "checkout/checkout_success.html", {"order": order})
