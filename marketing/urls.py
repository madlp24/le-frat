from django.urls import path
from . import views

urlpatterns = [
    path("newsletter/", views.newsletter_signup, name="newsletter_signup"),
    path("support/", views.support, name="support"),
    path("privacy/", views.privacy, name="privacy"),
    path("terms/", views.terms, name="terms"),
    path("about/", views.about, name="about"),
    path("faqs/", views.faqs, name="faqs"),
]
