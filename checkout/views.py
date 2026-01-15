import stripe
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import OrderForm
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_SECRET_KEY


def checkout(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.save()
            messages.success(request, "Order created. Payment successful.")
            return redirect("checkout_success")
        else:
            messages.error(request, "There was an error with your form.")
    else:
        form = OrderForm()

    intent = stripe.PaymentIntent.create(
        amount=1000,  # temporary fixed amount (we’ll calculate properly next)
        currency="usd",
    )

    context = {
        "order_form": form,
        "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
        "client_secret": intent.client_secret,
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