from django.contrib import admin
from .models import NewsletterSubscriber


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "source", "subscribed_at")
    list_filter = ("source", "subscribed_at")
    search_fields = ("email",)
    ordering = ("-subscribed_at",)
