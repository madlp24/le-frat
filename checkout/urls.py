from django.urls import path
from . import views

urlpatterns = [
    path("wh/", views.stripe_webhook, name="stripe_webhook"),
]
