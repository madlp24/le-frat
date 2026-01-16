from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from checkout.models import Order

@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user).order_by("-date")
    return render(request, "profiles/profile.html", {"orders": orders})
