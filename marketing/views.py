from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from .forms import NewsletterForm
from .models import NewsletterSubscriber
from django.shortcuts import render


def newsletter_signup(request):
    if request.method == "POST":
        form = NewsletterForm(request.POST)
        if form.is_valid():
            subscriber = form.save(commit=False)
            # Only accept a source we know about; the field is posted by a
            # hidden input, so never trust it as it arrives.
            posted = request.POST.get("source", NewsletterSubscriber.FOOTER)
            allowed = dict(NewsletterSubscriber.SOURCE_CHOICES)
            subscriber.source = (
                posted if posted in allowed else NewsletterSubscriber.FOOTER
            )
            subscriber.save()
            if subscriber.source == NewsletterSubscriber.MERCH:
                messages.success(request, _("You're on the list. We'll let you know."))
            else:
                messages.success(request, _("You're in. Welcome to the crew."))
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
