from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404
from checkout.models import Order

@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user).order_by("-date")
    return render(request, "profiles/profile.html", {"orders": orders})

@login_required
def order_detail(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, "profiles/order_detail.html", {"order": order})
