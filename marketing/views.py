from django.contrib import messages
from django.shortcuts import redirect
from .forms import NewsletterForm
from django.shortcuts import render

def newsletter_signup(request):
    if request.method == "POST":
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Subscribed successfully!")
        else:
            for error in form.errors.values():
                messages.error(request, error)

    return redirect(request.META.get("HTTP_REFERER", "/"))


def support(request):
    return render(request, "marketing/support.html")

def privacy(request):
    return render(request, "marketing/privacy.html")

def terms(request):
    return render(request, "marketing/terms.html")

def about(request):
    return render(request, "marketing/about.html")

def faqs(request):
    return render(request, "marketing/faqs.html")
