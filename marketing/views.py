from django.contrib import messages
from django.shortcuts import redirect
from .forms import NewsletterForm

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
