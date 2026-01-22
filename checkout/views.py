# checkout/views.py
import stripe
from decimal import Decimal, ROUND_HALF_UP

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Product


stripe.api_key = settings.STRIPE_SECRET_KEY


def checkout(request):
    bag = request.session.get("bag", {})
    if not bag:
        messages.error(request, "Your bag is empty.")
        return redirect("products")

    # calculate total
    total = Decimal("0.00")
    for item_id, quantity in bag.items():
        product = get_object_or_404(Product, pk=item_id)
        total += product.price * quantity

    # Stripe amount in cents (safe rounding)
    stripe_amount = int((total * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))

    if request.method == "POST":
        form = OrderForm(request.POST)

        # 🔑 Verify Stripe success BEFORE creating the order
        payment_intent_id = request.POST.get("payment_intent_id", "").strip()
        if not payment_intent_id:
            messages.error(request, "Payment was not completed. Please try again.")
            return redirect("checkout")

        try:
            pi = stripe.PaymentIntent.retrieve(payment_intent_id)
        except Exception:
            messages.error(request, "Could not verify payment. Please try again.")
            return redirect("checkout")

        if pi.status != "succeeded":
            messages.error(request, "Payment was not successful. Please try again.")
            return redirect("checkout")

        if int(pi.amount) != stripe_amount:
            messages.error(request, "Payment amount mismatch. Please try again.")
            return redirect("checkout")

        if form.is_valid():
            order = form.save(commit=False)
            order.order_total = total

            if request.user.is_authenticated:
                order.user = request.user

            order.save()

            for item_id, quantity in bag.items():
                product = get_object_or_404(Product, pk=item_id)
                line_total = product.price * quantity

                OrderLineItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    lineitem_total=line_total,
                )

            request.session["bag"] = {}
            messages.success(request, "Payment successful — order confirmed.")
            return redirect("checkout_success", order_number=order.order_number)

        messages.error(request, "There was an error with your form.")
        return redirect("checkout")

    # GET: create the PaymentIntent used by Stripe.js
    intent = stripe.PaymentIntent.create(
        amount=stripe_amount,
        currency="usd",
    )

    context = {
        "order_form": OrderForm(),
        "client_secret": intent.client_secret,
        "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
        "total": total,
    }
    return render(request, "checkout/checkout.html", context)


def checkout_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    # If the order belongs to a user, only that user can view it
    if order.user and (not request.user.is_authenticated or request.user != order.user):
        messages.error(request, "You do not have permission to view this order.")
        return redirect("home")

    return render(request, "checkout/checkout_success.html", {"order": order})